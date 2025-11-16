#!/usr/bin/env python3
"""
Quick portrait generator for test images using Flux
"""
import torch
from diffusers import FluxPipeline
from pathlib import Path

# Prompts for diverse character portraits
prompts = [
    "professional headshot portrait photo of a woman with brown hair, front facing, neutral expression, soft studio lighting, shoulders visible, sharp focus, high quality",
    "professional headshot portrait photo of a man with beard, front facing, slight smile, soft studio lighting, shoulders visible, sharp focus, high quality",
    "professional headshot portrait photo of a young woman with blonde hair, front facing, serious expression, soft studio lighting, shoulders visible, sharp focus, high quality",
    "professional headshot portrait photo of an older man with glasses, front facing, warm smile, soft studio lighting, shoulders visible, sharp focus, high quality",
]

def generate_portraits():
    """Generate test portrait images"""
    output_dir = Path("test_data/source")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Loading Flux model...")
    print("(This may take a minute...)")
    
    # Load Flux pipeline
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16
    )
    pipe.to("cuda")
    
    print("✅ Model loaded!\n")
    
    for i, prompt in enumerate(prompts, start=2):  # Start at 2 since we have test_01
        print(f"🎨 Generating test_{i:02d}...")
        print(f"   Prompt: {prompt[:60]}...")
        
        image = pipe(
            prompt,
            height=1024,
            width=1024,
            num_inference_steps=20,
            guidance_scale=3.5,
        ).images[0]
        
        output_path = output_dir / f"test_{i:02d}_flux_portrait.jpg"
        image.save(output_path, quality=95)
        print(f"   ✅ Saved: {output_path}\n")
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ All test portraits generated!")
    print(f"📁 Location: {output_dir}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    generate_portraits()
