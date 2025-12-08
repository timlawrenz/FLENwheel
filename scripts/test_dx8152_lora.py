#!/usr/bin/env python3
"""
Test dx8152 Multiple Angles LoRA for angle changes.
Compare with base model results.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from PIL import Image
import time

def test_lora():
    print("=" * 60)
    print("dx8152 Multiple Angles LoRA Test")
    print("=" * 60)
    
    base_model_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509"
    lora_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-edit-multiple-angles/镜头转换.safetensors"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    
    print(f"\n1. Loading base model...")
    start = time.time()
    
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        base_model_path,
        torch_dtype=torch.bfloat16
    )
    pipe.enable_sequential_cpu_offload()
    
    print(f"   ✅ Base model loaded in {time.time() - start:.1f}s\n")
    
    print(f"2. Loading LoRA weights...")
    start = time.time()
    
    try:
        pipe.load_lora_weights(lora_path)
        print(f"   ✅ LoRA loaded in {time.time() - start:.1f}s\n")
    except Exception as e:
        print(f"   ❌ Error loading LoRA: {e}")
        print(f"   Trying alternate method...\n")
        # Try loading from directory
        import os
        lora_dir = os.path.dirname(lora_path)
        try:
            pipe.load_lora_weights(lora_dir)
            print(f"   ✅ LoRA loaded from directory in {time.time() - start:.1f}s\n")
        except Exception as e2:
            print(f"   ❌ Also failed: {e2}")
            print(f"   Continuing without LoRA (will test base model)...\n")
    
    print(f"3. Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}\n")
    
    # Test different angle prompts (what dx8152 LoRA is trained for)
    angle_tests = [
        ("left_view", "Change camera angle to left side view, keep the person identical"),
        ("right_view", "Change camera angle to right side view, keep the person identical"),
        ("profile_left", "Show profile view from the left side, preserve facial features"),
        ("profile_right", "Show profile view from the right side, preserve facial features"),
        ("higher_angle", "Show from a higher camera angle looking down, keep features identical"),
        ("lower_angle", "Show from a lower camera angle looking up, keep features identical"),
    ]
    
    print(f"4. Generating {len(angle_tests)} angle variations...")
    print("=" * 60)
    
    results = []
    
    for idx, (name, prompt) in enumerate(angle_tests, 1):
        print(f"\n[{idx}/{len(angle_tests)}] {name}")
        print(f"Prompt: {prompt}")
        
        output_path = f"/home/tim/source/activity/FLENwheel/test_data/lora_test_{name}.png"
        
        start = time.time()
        
        try:
            with torch.inference_mode():
                output = pipe(
                    image=source_image,
                    prompt=prompt,
                    negative_prompt=" ",
                    num_inference_steps=40,
                    true_cfg_scale=4.0,
                    guidance_scale=1.0,
                    generator=torch.manual_seed(42),  # Fixed seed for consistency
                )
            
            result = output.images[0]
            result.save(output_path)
            
            elapsed = time.time() - start
            
            print(f"✅ Saved: {output_path}")
            print(f"   Time: {elapsed:.1f}s")
            
            results.append({
                "name": name,
                "prompt": prompt,
                "output": output_path,
                "time": elapsed,
                "success": True
            })
            
        except Exception as e:
            elapsed = time.time() - start
            
            print(f"❌ Error: {e}")
            print(f"   Time: {elapsed:.1f}s")
            
            results.append({
                "name": name,
                "prompt": prompt,
                "output": None,
                "time": elapsed,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\nTotal tests: {total}")
    print(f"Successful: {successful} ({successful/total*100:.1f}%)")
    print(f"Failed: {total - successful}")
    
    if successful > 0:
        avg_time = sum(r["time"] for r in results if r["success"]) / successful
        print(f"Average time per image: {avg_time:.1f}s")
    
    print(f"\n✅ Test complete!")
    print(f"\nGenerated images:")
    for r in results:
        if r["success"]:
            print(f"  - {r['output']}")
    
    print(f"\nCompare these angle variations with the source image to assess:")
    print(f"  - Character identity preservation")
    print(f"  - Angle change effectiveness")
    print(f"  - Image quality and artifacts")
    print()

if __name__ == "__main__":
    test_lora()
