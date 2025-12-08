#!/usr/bin/env python3
"""
Quick single test - render one image with one prompt to verify pipeline works.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from PIL import Image
import time

def quick_test():
    print("=" * 60)
    print("Quick Single Image Test")
    print("=" * 60)
    
    model_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    output_path = "/home/tim/source/activity/FLENwheel/test_data/quick_test.png"
    
    print(f"\n1. Loading model...")
    start = time.time()
    
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16
    )
    pipe.enable_sequential_cpu_offload()
    
    print(f"   ✅ Loaded in {time.time() - start:.1f}s\n")
    
    print(f"2. Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}\n")
    
    prompt = "Change background to a forest with trees, keep the person identical"
    print(f"3. Editing with prompt:")
    print(f"   '{prompt}'\n")
    
    start = time.time()
    
    with torch.inference_mode():
        output = pipe(
            image=source_image,
            prompt=prompt,
            negative_prompt=" ",  # Important: space, not empty
            num_inference_steps=40,
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            generator=torch.manual_seed(0),
        )
    
    elapsed = time.time() - start
    
    result = output.images[0]
    result.save(output_path)
    
    print(f"\n✅ Complete!")
    print(f"   Generation time: {elapsed:.1f}s")
    print(f"   Saved to: {output_path}")
    print()

if __name__ == "__main__":
    quick_test()
