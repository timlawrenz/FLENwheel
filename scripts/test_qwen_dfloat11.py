#!/usr/bin/env python3
"""
Test Qwen-Image-Edit-2509 with DFloat11 compression.
DFloat11: 32% smaller, lossless, fits on 24GB GPU with CPU offload.

Installation required:
    pip install dfloat11[cuda12]
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from PIL import Image
import time
import os

def test_dfloat11():
    print("=" * 60)
    print("Qwen-Image-Edit-2509 DFloat11 Compressed Test")
    print("=" * 60)
    
    # Check if dfloat11 is installed
    try:
        from dfloat11 import DFloat11Model
    except ImportError:
        print("\n❌ DFloat11 not installed!")
        print("\nInstall with:")
        print("    pip install dfloat11[cuda12]")
        print("\nThen run this script again.")
        return 1
    
    base_model_path = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model_path = "DFloat11/Qwen-Image-Edit-2509-DF11"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    output_path = "/home/tim/source/activity/FLENwheel/test_data/dfloat11_test.png"
    
    print(f"\n📊 DFloat11 Benefits:")
    print(f"   - 32% smaller (28GB vs 41GB)")
    print(f"   - Lossless (bit-identical outputs)")
    print(f"   - Fits on 24GB GPU with CPU offload")
    print(f"   - Faster than sequential CPU offload")
    
    print(f"\n1. Loading base model...")
    start = time.time()
    
    try:
        # Load base pipeline
        pipeline = QwenImageEditPlusPipeline.from_pretrained(
            base_model_path,
            torch_dtype=torch.bfloat16
        )
        
        print(f"   ✅ Base model loaded")
        
        # Apply DFloat11 compression to transformer
        print(f"\n2. Applying DFloat11 compression...")
        DFloat11Model.from_pretrained(
            dfloat11_model_path,
            bfloat16_model=pipeline.transformer,
            device="cpu",
            cpu_offload=True,  # Enable CPU offloading for 24GB GPU
            cpu_offload_blocks=20,  # Default value
            pin_memory=True,  # Enable for better performance
        )
        
        # Enable model CPU offloading for the pipeline
        pipeline.enable_model_cpu_offload()
        
        load_time = time.time() - start
        print(f"   ✅ DFloat11 compression applied in {load_time:.1f}s\n")
        
        # Check VRAM usage
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"   VRAM allocated: {allocated:.2f} GB")
            print(f"   VRAM reserved: {reserved:.2f} GB\n")
        
    except Exception as e:
        print(f"   ❌ Error loading DFloat11 model: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print(f"3. Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}\n")
    
    prompt = "Change background to a beach with ocean, keep the person identical"
    print(f"4. Editing with prompt:")
    print(f"   '{prompt}'\n")
    print(f"   Generating with DFloat11 compressed model...")
    
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
                generator=torch.manual_seed(42),
            )
        
        result = output.images[0]
        result.save(output_path)
        
        elapsed = time.time() - start
        
        # Get max memory usage
        if torch.cuda.is_available():
            max_memory = torch.cuda.max_memory_allocated(0) / 1024**3
        else:
            max_memory = 0
        
        print(f"\n✅ Complete!")
        print(f"   Generation time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        print(f"   Peak GPU memory: {max_memory:.2f} GB")
        print(f"   Saved to: {output_path}")
        
        print(f"\n" + "=" * 60)
        print("PERFORMANCE COMPARISON")
        print("=" * 60)
        
        print(f"\nBFloat16 (sequential CPU offload):")
        print(f"  - Model size: 54GB")
        print(f"  - Generation time: ~420s (7 minutes)")
        print(f"  - Method: Sequential component swapping")
        
        print(f"\nDFloat11 (block-level CPU offload):")
        print(f"  - Model size: 28GB (48% smaller)")
        print(f"  - Generation time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        print(f"  - Peak GPU memory: {max_memory:.2f} GB")
        print(f"  - Method: Block-level swapping with pinned memory")
        
        if elapsed < 420:
            speedup = 420 / elapsed
            print(f"\n⚡ Speedup: {speedup:.1f}x faster")
        
        print(f"\nCompare quality:")
        print(f"  - BFloat16: test_data/quick_test.png")
        print(f"  - DFloat11: {output_path}")
        print(f"  - Expected: Bit-identical (lossless compression)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(test_dfloat11())
