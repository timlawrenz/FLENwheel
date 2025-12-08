#!/usr/bin/env python3
"""
0I1 Character Enrichment - Phase 2: Pose Variations
Generate additional angles and poses using next-scene LoRA
"""

import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image
from pathlib import Path

SOURCE_DIR = Path.home() / "source/activity/FLENwheel/data/0I1/source"
OUTPUT_DIR = Path.home() / "source/activity/FLENwheel/data/0I1/enriched/poses"
QWEN_MODEL = "Qwen/Qwen-Image-Edit-2509"
NEXT_SCENE_LORA = Path.home() / "source/activity/FLENwheel/models/next-scene/next-scene_lora-v2-3000.safetensors"

# Pose variation prompts
POSE_PROMPTS = [
    # Sitting poses (missing from source)
    ("Next Scene: The person transitions to sitting on a chair, front view, neutral expression, clean background", "sitting_front", "fullbody_standing_frontleft.jpeg"),
    ("Next Scene: The person sits on a chair, side view showing full body, clean background", "sitting_side", "fullbody_standing_right.jpeg"),
    ("Next Scene: The person sits casually on a chair, three-quarter view, clean background", "sitting_threequarter", "fullbody_standing_modelpose_eyecontact.jpeg"),
    
    # Additional standing angles
    ("Next Scene: Camera rotates to show person standing, pure front view, arms at sides, clean background", "standing_front_pure", "fullbody_standing_frontleft.jpeg"),
    ("Next Scene: Camera rotates to show person standing, pure left side view, clean background", "standing_left_pure", "fullbody_standing_back_left.jpeg"),
    
    # T-pose (for model card)
    ("Next Scene: Person stands in T-pose with arms extended horizontally to sides, front view, clean background", "tpose_front", "fullbody_standing_frontleft.jpeg"),
    
    # Alternative kneeling angles
    ("Next Scene: Camera moves to front showing person kneeling, facing camera, clean background", "kneeling_front", "fullbody_kneeling_back_eyecontact.jpeg"),
    
    # Standing variations
    ("Next Scene: Person stands with hands clasped in front, front view, neutral expression, clean background", "standing_hands_front", "fullbody_standing_modelpose_eyecontact.jpeg"),
    ("Next Scene: Person stands relaxed, three-quarter right view, clean background", "standing_threequarter_right", "fullbody_standing_right.jpeg"),
    ("Next Scene: Person stands confidently, three-quarter left view, clean background", "standing_threequarter_left", "fullbody_standing_back_left.jpeg"),
]

def generate_poses():
    """Generate pose and angle variations"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("0I1 Pose Enrichment - Phase 2")
    print("=" * 70)
    print(f"\n📊 Pose variations to generate: {len(POSE_PROMPTS)}")
    print(f"💾 Output: {OUTPUT_DIR}\n")
    
    # Load pipeline
    print("🚀 Loading Qwen-Image-Edit + next-scene LoRA...")
    pipe = AutoPipelineForImage2Image.from_pretrained(
        QWEN_MODEL,
        torch_dtype=torch.bfloat16
    )
    pipe.load_lora_weights(str(NEXT_SCENE_LORA))
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    
    print("✅ Pipeline loaded\n")
    
    for idx, (prompt, name, source_file) in enumerate(POSE_PROMPTS, 1):
        source_path = SOURCE_DIR / source_file
        
        if not source_path.exists():
            print(f"[{idx}/{len(POSE_PROMPTS)}] ⚠️  Skipping {name} - source not found: {source_file}")
            continue
        
        print(f"[{idx}/{len(POSE_PROMPTS)}] Generating: {name}")
        print(f"    Source: {source_file}")
        print(f"    Prompt: {prompt[:60]}...")
        
        source_img = Image.open(source_path).convert("RGB")
        
        result = pipe(
            prompt=prompt,
            image=source_img,
            num_inference_steps=40,
            guidance_scale=7.0,
            attention_kwargs={"scale": 0.75}  # LoRA strength
        ).images[0]
        
        output_path = OUTPUT_DIR / f"0I1_pose_{name}.png"
        result.save(output_path)
        print(f"    ✅ Saved: {output_path.name}\n")
    
    print("=" * 70)
    print(f"🎉 Generated pose variations!")
    print(f"📁 Location: {OUTPUT_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    generate_poses()
