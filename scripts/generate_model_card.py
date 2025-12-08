#!/usr/bin/env python3
"""
Generate 23 benchmark images to test FLUX LoRA quality
Based on FLENwheel model card requirements:
- 20 portraits (5 angles × 4 expressions)
- 3 body poses
"""

import torch
from diffusers import FluxPipeline
from pathlib import Path
import sys

# Configuration
LORA_PATH = "/mnt/essdee/ai-toolkit/output/test_01_v1/test_01_v1.safetensors"
OUTPUT_DIR = Path.home() / "source/activity/FLENwheel/data/t01p/flux/v1/benchmark"
TRIGGER = "t01p"

# Model Card Portrait Prompts (20 total: 5 angles × 4 expressions)
ANGLES = ["front view", "half-left view", "left profile", "half-right view", "right profile"]
EXPRESSIONS = ["neutral expression", "genuine warm smile", "angry furrowed brow", "sad downcast eyes"]

PORTRAIT_BASE = "{trigger} person, {angle}, {expression}, clean white background, studio lighting, professional headshot, shoulders visible"

# Model Card Body Poses (3 total)
BODY_POSES = [
    f"{TRIGGER} person in T-pose with arms extended horizontally to sides, full body, front view, clean white background, studio lighting",
    f"{TRIGGER} person standing in neutral pose with arms relaxed at sides, full body, front view, clean white background, studio lighting",
    f"{TRIGGER} person sitting on simple chair, side view, full body, clean white background, studio lighting"
]

def generate_benchmark():
    """Generate all 23 model card benchmark images"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Loading FLUX.1-dev with LoRA (quantized for 24GB VRAM)...")
    from transformers import BitsAndBytesConfig
    
    # Use same settings as training config
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        transformer_kwargs={"quantization_config": nf4_config}
    )
    pipe.load_lora_weights(LORA_PATH)
    pipe.enable_model_cpu_offload()  # Additional VRAM optimization
    
    print("✅ Pipeline loaded\n")
    
    # Generate 20 portraits
    portrait_idx = 0
    for angle_idx, angle in enumerate(ANGLES):
        for expr_idx, expression in enumerate(EXPRESSIONS):
            prompt = PORTRAIT_BASE.format(
                trigger=TRIGGER,
                angle=angle,
                expression=expression
            )
            
            filename = f"portrait_{portrait_idx:02d}_{angle.replace(' ', '_').replace('-', '')}_{expression.split()[0]}.png"
            output_path = OUTPUT_DIR / filename
            
            print(f"[{portrait_idx+1}/23] Generating: {filename}")
            print(f"    Prompt: {prompt[:80]}...")
            
            image = pipe(
                prompt=prompt,
                num_inference_steps=20,
                guidance_scale=4.0,
                width=1024,
                height=1024,
                generator=torch.Generator("cuda").manual_seed(42 + portrait_idx)
            ).images[0]
            
            image.save(output_path)
            print(f"    ✅ Saved to {output_path}\n")
            
            portrait_idx += 1
    
    # Generate 3 body poses
    for pose_idx, prompt in enumerate(BODY_POSES):
        filename = f"pose_{20+pose_idx:02d}_{['tpose', 'standing', 'sitting'][pose_idx]}.png"
        output_path = OUTPUT_DIR / filename
        
        print(f"[{21+pose_idx}/23] Generating: {filename}")
        print(f"    Prompt: {prompt[:80]}...")
        
        image = pipe(
            prompt=prompt,
            num_inference_steps=20,
            guidance_scale=4.0,
            width=1024,
            height=1024,
            generator=torch.Generator("cuda").manual_seed(100 + pose_idx)
        ).images[0]
        
        image.save(output_path)
        print(f"    ✅ Saved to {output_path}\n")
    
    print(f"\n🎉 Generated 23/23 model card benchmark images")
    print(f"📁 Location: {OUTPUT_DIR}")
    print(f"\n📊 Next: Review images and score using evaluation checklist")

if __name__ == "__main__":
    generate_benchmark()
