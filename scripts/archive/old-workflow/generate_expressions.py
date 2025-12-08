#!/usr/bin/env python3
"""
Generate subtle facial expression variations using DFloat11.
Focus: Minimal changes (closed eyes, slight smile, relaxed) to help FLUX LoRA
learn the person without distorting identity.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from dfloat11 import DFloat11Model
from PIL import Image
import time
from pathlib import Path
from datetime import datetime

def generate_expression_variations():
    print("=" * 80)
    print("SUBTLE EYE GAZE VARIATIONS - Identity Preserving")
    print("=" * 80)
    
    # Paths
    base_model = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model = "DFloat11/Qwen-Image-Edit-2509-DF11"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(f"/home/tim/source/activity/FLENwheel/test_data/enriched/v1/batch_{timestamp}_gaze")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # SUBTLE expression changes only - keep identity intact!
    prompts = [
        # Eye gaze direction (very natural variations) - using "their left/right" for clarity
        ("looking_camera", "Make the person look directly at the camera, preserve the person's identity"),
        ("looking_their_left", "Make the person look to their left with their eyes, preserve identity"),
        ("looking_their_right", "Make the person look to their right with their eyes, preserve identity"),
        ("looking_up", "Make the person look upward with their eyes, preserve the person's identity"),
        ("looking_down", "Make the person look downward with their eyes, preserve identity"),
        ("looking_away", "Make the person look away naturally, preserve identity"),
        ("looking_their_upper_left", "Make the person look to their upper left, preserve the person's identity"),
        ("looking_their_upper_right", "Make the person look to their upper right, preserve identity"),
        ("looking_their_lower_left", "Make the person look to their lower left, preserve identity"),
        ("looking_their_lower_right", "Make the person look to their lower right, preserve the person's identity"),
        
        # Eyes closed/relaxed (minimal change)
        ("eyes_closed", "Make the person close their eyes gently, preserve the person's identity"),
        ("eyes_half_closed", "Make the person's eyes half-closed as if relaxed, preserve identity"),
        
        # Subtle mouth variations
        ("slight_smile", "Add a very slight natural smile, preserve identity"),
        ("lips_relaxed", "Make lips relaxed and neutral, preserve identity"),
        ("mouth_slightly_open", "Make mouth very slightly open naturally, preserve identity"),
    ]
    
    # Create README
    readme_content = f"""# Batch: Eye Gaze Direction Variations
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Generation Parameters
- **Source Image**: test_01.png
- **Model**: Qwen-Image-Edit-2509 with DFloat11 compression
- **LoRA**: None (base model only)
- **Method**: Eye gaze direction changes (NO angle/background changes)
- **Goal**: Help FLUX LoRA learn identity across minimal variations
- **Inference Steps**: 40
- **Seed**: 42 + image_index (varied per image)

## Strategy: Eye Gaze Direction
Focus on **where the person is looking** - extremely subtle but powerful:
- Different eye directions (left, right, up, down, diagonals)
- Eyes open vs closed variations
- Minimal mouth changes

This prevents:
- ❌ Facial distortion
- ❌ Identity drift
- ❌ Unrealistic changes

This enables:
- ✅ FLUX LoRA learns "same person, different states"
- ✅ Better generalization
- ✅ High identity preservation

## Prompts Used ({len(prompts)} variations)

### Eye Gaze Direction (10) - Core variations
- looking_camera: Looking directly at camera
- looking_their_left: Eyes looking to their left
- looking_their_right: Eyes looking to their right
- looking_up: Eyes looking upward
- looking_down: Eyes looking downward
- looking_away: Looking away naturally
- looking_their_upper_left: Eyes to their upper left
- looking_their_upper_right: Eyes to their upper right
- looking_their_lower_left: Eyes to their lower left
- looking_their_lower_right: Eyes to their lower right

### Eyes Closed/Relaxed (2)
- eyes_closed: Eyes gently closed
- eyes_half_closed: Relaxed, half-closed eyes

### Subtle Mouth (3)
- slight_smile: Very slight natural smile
- lips_relaxed: Relaxed, neutral lips
- mouth_slightly_open: Slightly open mouth

## Quality Criteria
When reviewing, accept images that:
- ✅ Clearly show the same person
- ✅ Have natural, subtle changes
- ✅ Preserve freckles, skin texture, face shape
- ✅ Look believable and realistic

Reject images that:
- ❌ Change face shape or features
- ❌ Add/remove freckles or skin details
- ❌ Look artificial or distorted
- ❌ Don't match the requested subtle change

## Decision
- [ ] Accept for training dataset
- [ ] Needs review
- [ ] Reject (reason: ________________)
"""
    
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created batch folder: {output_dir.name}")
    print(f"✅ Created README: {readme_path}")
    
    print(f"\n📋 Generation Plan:")
    print(f"   Source: test_01.png")
    print(f"   Total variations: {len(prompts)}")
    print(f"   Focus: Eye gaze direction changes (identity preserving)")
    print(f"   Method: DFloat11 (no LoRA complexity)")
    print(f"   Estimated time: ~{len(prompts) * 3.8:.0f} minutes ({len(prompts) * 3.8 / 60:.1f} hours)")
    
    proceed = input(f"\n⏱️  This will take ~{len(prompts) * 3.8 / 60:.1f} hours. Proceed? (y/n): ")
    if proceed.lower() != 'y':
        print("Aborted.")
        return
    
    print(f"\n" + "=" * 80)
    print("Loading Model (DFloat11)")
    print("=" * 80)
    
    start = time.time()
    
    # Load pipeline with DFloat11
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16
    )
    
    DFloat11Model.from_pretrained(
        dfloat11_model,
        bfloat16_model=pipeline.transformer,
        device="cpu",
        cpu_offload=True,
        cpu_offload_blocks=20,
        pin_memory=True,
    )
    
    pipeline.enable_model_cpu_offload()
    
    load_time = time.time() - start
    print(f"✅ Model loaded in {load_time:.1f}s\n")
    
    # Load source image
    source_image = Image.open(source_path)
    print(f"✅ Source image loaded: {source_path}")
    print(f"   Size: {source_image.size}\n")
    
    # Generate variations
    results = []
    
    for idx, (name, prompt) in enumerate(prompts, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(prompts)}] {name}")
        print(f"{'='*80}")
        print(f"Prompt: {prompt}")
        
        output_path = output_dir / f"{name}.png"
        
        start = time.time()
        
        try:
            with torch.inference_mode():
                output = pipeline(
                    image=[source_image],
                    prompt=prompt,
                    negative_prompt=" ",
                    num_inference_steps=40,
                    true_cfg_scale=4.0,
                    guidance_scale=1.0,
                    generator=torch.manual_seed(42 + idx),  # Vary seed
                )
            
            result = output.images[0]
            result.save(output_path)
            
            elapsed = time.time() - start
            
            print(f"✅ Saved: {output_path.name}")
            print(f"⏱️  Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
            
            results.append({
                "name": name,
                "output": output_path,
                "time": elapsed,
                "success": True
            })
            
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ Error: {e}")
            results.append({
                "name": name,
                "output": None,
                "time": elapsed,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    
    successful = sum(1 for r in results if r["success"])
    total_time = sum(r["time"] for r in results)
    
    print(f"\n✅ Successful: {successful}/{len(prompts)}")
    print(f"⏱️  Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"📁 Output: {output_dir}")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Review images in {output_dir}")
    print(f"   2. Check if gaze changed WITHOUT identity loss")
    print(f"   3. Accept images that show same person with minor variations")
    print(f"   4. These help FLUX LoRA learn identity across different states")
    print()

if __name__ == "__main__":
    generate_expression_variations()
