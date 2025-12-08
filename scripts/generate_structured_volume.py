#!/usr/bin/env python3
"""
Structured Volume Generation Orchestrator

Loads YAML templates and generates images using multiple models in parallel.
Designed for AMD 7995X (128GB VRAM) with 4-6 models running concurrently.

Usage:
    python generate_structured_volume.py \\
        --character character-001 \\
        --categories portraits,body-poses,context,hands \\
        --parallel 4
"""

import argparse
import json
import logging
import os
import sys
import time
import yaml
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading

# ML libraries
import torch
from diffusers import QwenImageEditPlusPipeline
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# NAS paths
NAS_ROOT = Path("/mnt/nas-ai-models")
TRAINING_DATA = NAS_ROOT / "training-data" / "flenwheel"
TEMPLATES_DIR = TRAINING_DATA / "templates"
SOURCES_DIR = TRAINING_DATA / "sources"
GENERATED_DIR = TRAINING_DATA / "generated"

# Model paths (shared on NAS - accessible from both RTX 4090 and AMD servers)
QWEN_BASE_PATH = "/mnt/nas-ai-models/diffusion_models/qwen-image-edit-2509"
QWEN_ANGLES_PATH = "/mnt/nas-ai-models/diffusion_models/qwen-edit-multiple-angles"

@dataclass
class GenerationTask:
    """Single image generation task"""
    category: str
    template_name: str
    prompt: str
    model_name: str
    lora_name: Optional[str]
    source_images: List[Path]
    seed: int
    output_path: Path
    metadata_path: Path

@dataclass
class GenerationResult:
    """Result of a generation task"""
    task: GenerationTask
    success: bool
    duration: float
    error: Optional[str] = None

class TemplateLoader:
    """Loads and expands YAML templates"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        
    def load_template(self, category: str) -> Dict[str, Any]:
        """Load template YAML for a category"""
        template_path = self.templates_dir / f"{category}.yaml"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        with open(template_path, 'r') as f:
            return yaml.safe_load(f)
    
    def expand_prompts(self, template_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Expand template variables into concrete prompts"""
        expanded = []
        
        for template_name, template_config in template_data.get('templates', {}).items():
            prompt_template = template_config['prompt']
            variations = template_config.get('variations', {})
            
            if not variations:
                # No variations, just use the prompt as-is
                expanded.append({
                    'template_name': template_name,
                    'prompt': prompt_template,
                    'variables': {}
                })
                continue
            
            # Generate all combinations of variations
            var_names = list(variations.keys())
            var_values = [variations[name] for name in var_names]
            
            for combination in product(*var_values):
                var_dict = dict(zip(var_names, combination))
                
                # Substitute variables in prompt
                prompt = prompt_template
                for var_name, var_value in var_dict.items():
                    prompt = prompt.replace(f'{{{var_name}}}', var_value)
                
                expanded.append({
                    'template_name': template_name,
                    'prompt': prompt,
                    'variables': var_dict
                })
        
        logger.info(f"Expanded {len(expanded)} prompts from template")
        return expanded

class ModelManager:
    """Manages model loading and VRAM"""
    
    def __init__(self, max_models: int = 4, max_vram_gb: int = 24):
        self.max_models = max_models
        self.max_vram_gb = max_vram_gb  # RTX 4090: 24GB
        self.loaded_models = {}
        self.vram_usage_gb = 0
        self.lock = threading.Lock()
        
        # Model path mapping
        self.model_paths = {
            'qwen-base': QWEN_BASE_PATH,
            'qwen-angles': QWEN_ANGLES_PATH,
            'qwen-lighting': QWEN_BASE_PATH,  # Same as base for now
            'flux2-multiref': None,  # TODO: Add FLUX.2 support
        }
    
    def load_model(self, model_name: str, lora_name: Optional[str] = None):
        """Load a model with Diffusers"""
        model_key = f"{model_name}_{lora_name or 'base'}"
        
        with self.lock:
            if model_key in self.loaded_models:
                return model_key
            
            model_path = self.model_paths.get(model_name)
            if model_path is None:
                logger.warning(f"Model {model_name} not yet supported, skipping")
                return None
            
            logger.info(f"Loading model: {model_key} from {model_path}")
            
            try:
                # Load Qwen-Image-Edit pipeline with CPU offloading for RTX 4090
                pipeline = QwenImageEditPlusPipeline.from_pretrained(
                    model_path,
                    torch_dtype=torch.bfloat16
                )
                
                # Memory optimizations for RTX 4090 (24GB VRAM limit)
                # Use sequential CPU offload instead of model offload for better memory control
                pipeline.enable_sequential_cpu_offload()
                
                # Critical: Reduce VRAM during inference
                pipeline.enable_attention_slicing()  # Slice attention computation
                if hasattr(pipeline, 'vae'):
                    pipeline.vae.enable_tiling()  # Tile VAE for lower VRAM
                
                logger.info(f"Pipeline loaded with sequential CPU offload + memory optimizations")
                
                # Estimate VRAM (conservative)
                estimated_vram = 15  # GB, conservative estimate for Qwen with offloading
                
                if self.vram_usage_gb + estimated_vram > self.max_vram_gb:
                    logger.warning(f"Insufficient VRAM: {self.vram_usage_gb + estimated_vram}GB exceeds {self.max_vram_gb}GB")
                    # Don't raise error, just don't load more models
                    return None
                
                self.loaded_models[model_key] = {
                    'pipeline': pipeline,
                    'model_name': model_name,
                    'lora_name': lora_name,
                    'vram_gb': estimated_vram
                }
                self.vram_usage_gb += estimated_vram
                
                logger.info(f"✓ Model loaded successfully, VRAM: {self.vram_usage_gb}/{self.max_vram_gb}GB")
                
            except Exception as e:
                logger.error(f"Failed to load model {model_key}: {e}")
                return None
                
        return model_key
    
    def get_pipeline(self, model_key: str):
        """Get loaded pipeline"""
        return self.loaded_models.get(model_key, {}).get('pipeline')
    
    def get_vram_usage(self) -> Dict[str, float]:
        """Get current VRAM usage statistics"""
        return {
            'total_gb': self.max_vram_gb,
            'used_gb': self.vram_usage_gb,
            'available_gb': self.max_vram_gb - self.vram_usage_gb,
            'utilization_pct': (self.vram_usage_gb / self.max_vram_gb) * 100
        }

class GenerationOrchestrator:
    """Coordinates parallel image generation"""
    
    def __init__(self, character_id: str, parallel_workers: int = 4):
        self.character_id = character_id
        self.parallel_workers = parallel_workers
        self.template_loader = TemplateLoader(TEMPLATES_DIR)
        self.model_manager = ModelManager(max_models=parallel_workers)
        self.task_queue = Queue()
        self.results = []
        
        # Paths for this character
        self.source_dir = SOURCES_DIR / character_id
        self.output_dir = GENERATED_DIR / character_id
        
        # Verify source images exist
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
        
        self.source_images = list(self.source_dir.glob("*.png")) + list(self.source_dir.glob("*.jpg"))
        if not self.source_images:
            raise ValueError(f"No source images found in {self.source_dir}")
        
        logger.info(f"Found {len(self.source_images)} source images")
    
    def generate_tasks(self, categories: List[str], seeds_per_prompt: int = 1) -> List[GenerationTask]:
        """Generate all tasks from templates"""
        all_tasks = []
        
        for category in categories:
            logger.info(f"Loading template: {category}")
            template_data = self.template_loader.load_template(category)
            
            # Expand prompts
            expanded_prompts = self.template_loader.expand_prompts(template_data)
            
            # Get models for this category
            models = template_data.get('models', ['qwen-base'])
            
            # Create output directory for category
            category_dir = self.output_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate tasks for each prompt × model × seed
            task_id = 0
            for prompt_data in expanded_prompts:
                for model_name in models:
                    for seed_idx in range(seeds_per_prompt):
                        seed = 1000000 + task_id + seed_idx
                        
                        # Determine LoRA if model specifies it
                        lora_name = None
                        if 'lora' in model_name:
                            lora_name = model_name
                            model_name = 'qwen-base'  # Base model name
                        
                        # Output filename
                        filename = f"{category}_{prompt_data['template_name']}_{model_name.replace('-', '_')}_{seed:08d}.png"
                        output_path = category_dir / filename
                        metadata_path = output_path.with_suffix('.json')
                        
                        task = GenerationTask(
                            category=category,
                            template_name=prompt_data['template_name'],
                            prompt=prompt_data['prompt'],
                            model_name=model_name,
                            lora_name=lora_name,
                            source_images=self.source_images,
                            seed=seed,
                            output_path=output_path,
                            metadata_path=metadata_path
                        )
                        
                        # Skip if already generated
                        if output_path.exists():
                            logger.debug(f"Skipping existing: {filename}")
                            continue
                        
                        all_tasks.append(task)
                        task_id += 1
        
        logger.info(f"Generated {len(all_tasks)} tasks across {len(categories)} categories")
        return all_tasks
    
    def execute_task(self, task: GenerationTask) -> GenerationResult:
        """Execute a single generation task"""
        start_time = time.time()
        
        try:
            # Load model (if not already loaded)
            model_key = self.model_manager.load_model(task.model_name, task.lora_name)
            
            if model_key is None:
                raise ValueError(f"Failed to load model: {task.model_name}")
            
            # Get pipeline
            pipeline = self.model_manager.get_pipeline(model_key)
            if pipeline is None:
                raise ValueError(f"Pipeline not found for {model_key}")
            
            # Select random source image
            source_image_path = random.choice(task.source_images)
            source_image = Image.open(source_image_path)
            
            logger.info(f"Generating: {task.output_path.name} (source: {source_image_path.name})")
            
            # Generate image
            with torch.inference_mode():
                output = pipeline(
                    image=source_image,
                    prompt=task.prompt,
                    negative_prompt=" ",  # Important: space, not empty
                    num_inference_steps=40,
                    true_cfg_scale=4.0,
                    guidance_scale=1.0,
                    generator=torch.manual_seed(task.seed),
                )
            
            result_image = output.images[0]
            
            # Save image
            result_image.save(task.output_path)
            
            # Save metadata
            metadata = {
                'category': task.category,
                'template_name': task.template_name,
                'prompt': task.prompt,
                'model_name': task.model_name,
                'lora_name': task.lora_name,
                'source_image': str(source_image_path),
                'source_images_available': [str(p) for p in task.source_images],
                'seed': task.seed,
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'output_path': str(task.output_path),
                'inference_steps': 40,
                'true_cfg_scale': 4.0,
                'guidance_scale': 1.0
            }
            
            with open(task.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            duration = time.time() - start_time
            logger.info(f"✓ Generated {task.output_path.name} in {duration:.1f}s")
            
            return GenerationResult(
                task=task,
                success=True,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"✗ Failed {task.output_path.name}: {e}")
            
            # Clean up VRAM after failure to prevent accumulation
            if 'CUDA out of memory' in str(e) or 'Expected all tensors' in str(e):
                import gc
                gc.collect()
                torch.cuda.empty_cache()
                logger.info("Cleaned up GPU memory after failure")
            
            return GenerationResult(
                task=task,
                success=False,
                duration=duration,
                error=str(e)
            )
    
    def run(self, categories: List[str], seeds_per_prompt: int = 1):
        """Run the orchestrator"""
        logger.info(f"Starting orchestrator for character: {self.character_id}")
        logger.info(f"Categories: {', '.join(categories)}")
        logger.info(f"Parallel workers: {self.parallel_workers}")
        
        # Generate all tasks
        tasks = self.generate_tasks(categories, seeds_per_prompt)
        
        if not tasks:
            logger.info("No tasks to execute (all images already generated)")
            return
        
        logger.info(f"Executing {len(tasks)} tasks with {self.parallel_workers} workers")
        
        # Execute tasks in parallel
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            futures = {executor.submit(self.execute_task, task): task for task in tasks}
            
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)
                completed += 1
                
                if completed % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    remaining = len(tasks) - completed
                    eta = remaining / rate if rate > 0 else 0
                    
                    vram = self.model_manager.get_vram_usage()
                    logger.info(f"Progress: {completed}/{len(tasks)} ({completed/len(tasks)*100:.1f}%) | "
                              f"Rate: {rate:.2f} img/s | ETA: {eta/60:.1f}min | "
                              f"VRAM: {vram['utilization_pct']:.1f}%")
        
        # Summary
        total_time = time.time() - start_time
        success_count = sum(1 for r in self.results if r.success)
        
        logger.info("="*80)
        logger.info(f"Generation complete!")
        logger.info(f"Total time: {total_time/60:.1f} minutes")
        logger.info(f"Success: {success_count}/{len(tasks)} ({success_count/len(tasks)*100:.1f}%)")
        logger.info(f"Average: {len(tasks)/total_time:.2f} images/second")
        logger.info(f"Output: {self.output_dir}")
        logger.info("="*80)

def main():
    parser = argparse.ArgumentParser(description="Structured Volume Generation Orchestrator")
    parser.add_argument('--character', required=True, help="Character ID (e.g., character-001)")
    parser.add_argument('--categories', default='portraits,body-poses,context,hands',
                       help="Comma-separated list of categories")
    parser.add_argument('--parallel', type=int, default=4,
                       help="Number of parallel workers (models)")
    parser.add_argument('--seeds', type=int, default=1,
                       help="Number of seed variations per prompt")
    
    args = parser.parse_args()
    
    categories = [c.strip() for c in args.categories.split(',')]
    
    # Verify NAS mount
    if not NAS_ROOT.exists():
        logger.error(f"NAS not mounted at {NAS_ROOT}")
        sys.exit(1)
    
    # Create orchestrator and run
    orchestrator = GenerationOrchestrator(
        character_id=args.character,
        parallel_workers=args.parallel
    )
    
    orchestrator.run(categories, seeds_per_prompt=args.seeds)

if __name__ == '__main__':
    main()
