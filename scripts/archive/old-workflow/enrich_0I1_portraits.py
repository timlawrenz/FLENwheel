#!/usr/bin/env python3
"""
0I1 Character Enrichment - Phase 1: Portrait Close-ups
Generate clean portrait variations using next-scene LoRA
"""

import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image
from pathlib import Path
import gc

# Configuration
SOURCE_DIR = Path.home() / "source/activity/FLENwheel/data/0I1/source"
OUTPUT_DIR = Path.home() / "source/activity/FLENwheel/data/0I1/enriched/portraits"
QWEN_MODEL = "Qwen/Qwen-Image-Edit-2509"
NEXT_SCENE_LORA = Path.home() / "source/activity/FLENwheel/models/next-scene/next-scene_lora-v2-3000.safetensors"

# Portrait prompts for missing angles
PORTRAIT_PROMPTS = [
    # Front portraits
    ("Next Scene: Camera moves in for a close-up portrait, front view of the person's face, neutral expression, clean background", "front_neutral"),
    ("Next Scene: Camera moves in for a close-up portrait, front view of the person's face, soft smile, clean background", "front_smile"),
    ("Next Scene: Camera moves in for a close-up portrait, front view of the person's face, serious expression, clean background", "front_serious"),
    
    # Half-left portraits
    ("Next Scene: Camera moves to a 45-degree angle showing the person's left side, half-left portrait view, neutral expression, clean background", "halfleft_neutral"),
    ("Next Scene: Camera moves to a 45-degree angle showing the person's left side, half-left portrait view, soft smile, clean background", "halfleft_smile"),
    
    # Left profile
    ("Next Scene: Camera moves to the left side, showing person's left profile view, neutral expression, clean background", "leftprofile_neutral"),
    ("Next Scene: Camera moves to the left side, showing person's left profile view, soft smile, clean background", "leftprofile_smile"),
    
    # Half-right portraits
    ("Next Scene: Camera moves to a 45-degree angle showing the person's right side, half-right portrait view, neutral expression, clean background", "halfright_neutral"),
    ("Next Scene: Camera moves to a 45-degree angle showing the person's right side, half-right portrait view, soft smile, clean background", "halfright_smile"),
    
    # Right profile
    ("Next Scene: Camera moves to the right side, showing person's right profile view, neutral expression, clean background", "rightprofile_neutral"),
    ("Next Scene: Camera moves to the right side, showing person's right profile view, soft smile, clean background", "rightprofile_smile"),
]

def generate_portraits():
    """Generate portrait variations from best source images"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Select best source images with faces visible
    best_sources = [
        SOURCE_DIR / "ig2qkp2h2rn12zqzqcor6bprwq8s_eyecontact.jpeg",
        SOURCE_DIR / "k6jbijfbfsya0mclsdifpp1cnett.jpeg",
        SOURCE_DIR / "fullbody_standing_modelpose_eyecontact.jpeg",
    ]
    
    # Filter to existing files
    sources = [s for s in best_sources if s.exists()]
    if not sources:
        print("⚠️  No suitable source images found!")
        return
    
    print("=" * 70)
    print("0I1 Portrait Enrichment - Phase 1")
    print("=" * 70)
    print(f"\n📁 Source images: {len(sources)}")
    print(f"📊 Portraits to generate: {len(PORTRAIT_PROMPTS)}")
    print(f"💾 Output: {OUTPUT_DIR}\n")
    
    # Load pipeline with next-scene LoRA
    print("🚀 Loading Qwen-Image-Edit + next-scene LoRA...")
    pipe = AutoPipelineForImage2Image.from_pretrained(
        QWEN_MODEL,
        torch_dtype=torch.bfloat16
    )
    pipe.load_lora_weights(str(NEXT_SCENE_LORA))
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    
    print("✅ Pipeline loaded\n")
    
    # Generate portraits from first source
    source_img = Image.open(sources[0]).convert("RGB")
    
    for idx, (prompt, name) in enumerate(PORTRAIT_PROMPTS, 1):
        print(f"[{idx}/{len(PORTRAIT_PROMPTS)}] Generating: {name}")
        print(f"    Prompt: {prompt[:60]}...")
        
        result = pipe(
            prompt=prompt,
            image=source_img,
            num_inference_steps=40,
            guidance_scale=7.0,
            attention_kwargs={"scale": 0.75}  # LoRA strength
        ).images[0]
        
        output_path = OUTPUT_DIR / f"0I1_portrait_{name}.png"
        result.save(output_path)
        print(f"    ✅ Saved: {output_path.name}\n")
    
    print("=" * 70)
    print(f"🎉 Generated {len(PORTRAIT_PROMPTS)} portrait variations!")
    print(f"📁 Location: {OUTPUT_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    generate_portraits()
