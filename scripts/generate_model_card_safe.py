#!/usr/bin/env python3
"""
Generate model card benchmarks ONE AT A TIME with memory cleanup
Slower but works on 24GB VRAM
"""

import torch
from diffusers import FluxPipeline
from pathlib import Path
import gc

LORA_PATH = "/mnt/essdee/ai-toolkit/output/test_01_v1/test_01_v1_000002500.safetensors"
OUTPUT_DIR = Path.home() / "source/activity/FLENwheel/data/t01p/flux/v1/benchmark"
TRIGGER = "t01p"

# Model Card Prompts
ANGLES = ["front view", "half-left view", "left profile", "half-right view", "right profile"]
EXPRESSIONS = ["neutral expression", "genuine warm smile", "angry furrowed brow", "sad downcast eyes"]
PORTRAIT_BASE = "{trigger} person, {angle}, {expression}, clean white background, studio lighting, professional headshot, shoulders visible"

BODY_POSES = [
    f"{TRIGGER} person in T-pose with arms extended horizontally to sides, full body, front view, clean white background, studio lighting",
    f"{TRIGGER} person standing in neutral pose with arms relaxed at sides, full body, front view, clean white background, studio lighting",
    f"{TRIGGER} person sitting on simple chair, side view, full body, clean white background, studio lighting"
]

def generate_single(prompt, filename, seed):
    """Generate single image with full cleanup"""
    print(f"\n🚀 Loading pipeline...")
    
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16
    )
    pipe.load_lora_weights(LORA_PATH)
    pipe.enable_sequential_cpu_offload()  # More aggressive offloading
    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    
    print(f"✅ Generating: {filename}")
    print(f"   Prompt: {prompt[:70]}...")
    
    image = pipe(
        prompt=prompt,
        num_inference_steps=20,
        guidance_scale=4.0,
        width=1024,
        height=1024,
        generator=torch.Generator("cuda").manual_seed(seed)
    ).images[0]
    
    output_path = OUTPUT_DIR / filename
    image.save(output_path)
    print(f"   ✅ Saved: {output_path}")
    
    # Aggressive cleanup
    del pipe
    gc.collect()
    torch.cuda.empty_cache()
    print(f"   🧹 Cleaned up memory\n")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("FLENwheel Model Card Benchmark Generator")
    print("=" * 70)
    print("\n⚠️  ONE image at a time to avoid OOM")
    print(f"📁 Output: {OUTPUT_DIR}\n")
    
    # Generate 20 portraits
    portrait_idx = 0
    for angle in ANGLES:
        for expression in EXPRESSIONS:
            prompt = PORTRAIT_BASE.format(trigger=TRIGGER, angle=angle, expression=expression)
            filename = f"portrait_{portrait_idx:02d}_{angle.replace(' ', '_').replace('-', '')}_{expression.split()[0]}.png"
            
            print(f"[{portrait_idx+1}/23]", end=" ")
            generate_single(prompt, filename, seed=42 + portrait_idx)
            portrait_idx += 1
    
    # Generate 3 body poses
    for pose_idx, prompt in enumerate(BODY_POSES):
        filename = f"pose_{20+pose_idx:02d}_{['tpose', 'standing', 'sitting'][pose_idx]}.png"
        print(f"[{21+pose_idx}/23]", end=" ")
        generate_single(prompt, filename, seed=100 + pose_idx)
    
    print("\n" + "=" * 70)
    print(f"🎉 Generated 23/23 model card benchmark images!")
    print(f"📁 Location: {OUTPUT_DIR}")
    print(f"\n📊 Next: Review and score using:")
    print(f"   ~/source/activity/FLENwheel/data/t01p/flux/v1/EVALUATION_CHECKLIST.md")
    print("=" * 70)

if __name__ == "__main__":
    main()
