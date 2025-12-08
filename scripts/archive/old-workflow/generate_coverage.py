#!/usr/bin/env python3
"""
Generate targeted angle variations from test_04.png to fill coverage gaps.
Focus: Right-facing angles and profile views.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from dfloat11 import DFloat11Model
from PIL import Image
import time
from pathlib import Path

def generate_coverage_images():
    print("=" * 80)
    print("TARGETED GENERATION - Fill Coverage Gaps")
    print("=" * 80)
    
    # Paths
    base_model = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model = "DFloat11/Qwen-Image-Edit-2509-DF11"
    lora_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-edit-multiple-angles/镜头转换.safetensors"
    
    # Source image (ONE person only!)
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    
    output_dir = Path("/home/tim/source/activity/FLENwheel/test_data/coverage")
    output_dir.mkdir(exist_ok=True)
    
    # Focus on missing angles (especially RIGHT-facing) and scene variety
    all_prompts = [
        # PRIORITY: Right-facing angles (currently missing!)
        ("right_half", "Change camera angle to right side view showing right cheek, keep the person identical"),
        ("right_profile", "Show right profile view from the side, preserve facial features exactly"),
        ("right_quarter", "Show the person from slight right angle, maintain appearance"),
        
        # More angle variety
        ("front_neutral", "Show the person facing directly forward, neutral expression, keep identity identical"),
        ("front_slight_smile", "Show the person facing forward with a slight smile, keep identity identical"),
        
        # Background/lighting variations for diversity
        ("studio_lighting", "Add professional studio lighting with clean background, keep person identical"),
        ("urban_background", "Change background to urban city setting, keep person identical"),
        ("indoor_home", "Change background to cozy indoor home setting, keep person identical"),
        ("sunset_outdoor", "Add warm sunset lighting outdoors, keep person identical"),
        ("night_city", "Change background to nighttime city with lights, keep person identical"),
    ]
    
    print(f"\n📋 Generation Plan:")
    print(f"   Source: test_01.png (ONE person only)")
    print(f"   Total prompts: {len(all_prompts)}")
    print(f"   Focus: Right-facing angles + scene variety")
    print(f"   Estimated time: ~{len(all_prompts) * 3.8:.0f} minutes ({len(all_prompts) * 3.8 / 60:.1f} hours)")
    
    proceed = input(f"\n⏱️  This will take ~{len(all_prompts) * 3.8 / 60:.1f} hours. Proceed? (y/n): ")
    if proceed.lower() != 'y':
        print("Aborted.")
        return
    
    print(f"\n" + "=" * 80)
    print("Loading Model")
    print("=" * 80)
    
    start = time.time()
    
    # Load base pipeline
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16
    )
    
    # Apply DFloat11 compression FIRST
    print(f"Applying DFloat11 compression...")
    DFloat11Model.from_pretrained(
        dfloat11_model,
        bfloat16_model=pipeline.transformer,
        device="cpu",
        cpu_offload=True,
        cpu_offload_blocks=20,
        pin_memory=True,
    )
    
    pipeline.enable_model_cpu_offload()
    
    # THEN load LoRA on top of compressed model
    print(f"Loading LoRA weights...")
    pipeline.load_lora_weights(lora_path)
    print(f"✅ LoRA loaded")
    
    load_time = time.time() - start
    print(f"✅ Model + DFloat11 + LoRA loaded in {load_time:.1f}s\n")
    
    # Load source image
    source_image = Image.open(source_path)
    print(f"✅ Source image loaded: {source_path}")
    
    # Generate images
    results = []
    
    for idx, (name, prompt) in enumerate(all_prompts, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(all_prompts)}] {name}")
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
    
    print(f"\n✅ Successful: {successful}/{len(all_prompts)}")
    print(f"⏱️  Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"📁 Output: {output_dir}")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Review all images in {output_dir}")
    print(f"   2. Move good ones to data/enriched/v1/good/")
    print(f"   3. Count total good images")
    print(f"   4. If ≥30 good images → Ready for FLUX training!")
    print()

if __name__ == "__main__":
    generate_coverage_images()
