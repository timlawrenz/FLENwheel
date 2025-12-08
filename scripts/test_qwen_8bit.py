#!/usr/bin/env python3
"""
Test Qwen-Image-Edit-2509 with 8-bit quantization using bitsandbytes.
This uses standard int8 quantization instead of GGUF.
"""

import torch
from diffusers import QwenImageEditPlusPipeline, BitsAndBytesConfig
from PIL import Image
import time

def test_8bit_quantized():
    print("=" * 60)
    print("Qwen-Image-Edit-2509 8-bit Quantized Test (bitsandbytes)")
    print("=" * 60)
    
    base_model_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    output_path = "/home/tim/source/activity/FLENwheel/test_data/quantized_8bit_test.png"
    
    print(f"\n1. Loading 8-bit quantized model...")
    print(f"   Using bitsandbytes int8 quantization")
    print(f"   Expected: Fits in GPU VRAM, 2-3x faster")
    
    start = time.time()
    
    try:
        # Create 8-bit quantization config
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_compute_dtype=torch.bfloat16,
        )
        
        print(f"\n   Loading with 8-bit quantization...")
        
        pipe = QwenImageEditPlusPipeline.from_pretrained(
            base_model_path,
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16,
        )
        
        load_time = time.time() - start
        print(f"   ✅ Model loaded in {load_time:.1f}s\n")
        
        # Check VRAM usage
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"   VRAM allocated: {allocated:.2f} GB")
            print(f"   VRAM reserved: {reserved:.2f} GB\n")
        
    except Exception as e:
        print(f"   ❌ Error loading 8-bit model: {e}")
        print(f"\n   Trying 4-bit quantization instead...")
        
        try:
            # Try 4-bit as alternative
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            
            pipe = QwenImageEditPlusPipeline.from_pretrained(
                base_model_path,
                quantization_config=quantization_config,
                torch_dtype=torch.bfloat16,
            )
            
            load_time = time.time() - start
            print(f"   ✅ Model loaded with 4-bit quantization in {load_time:.1f}s\n")
            
            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated(0) / 1024**3
                reserved = torch.cuda.memory_reserved(0) / 1024**3
                print(f"   VRAM allocated: {allocated:.2f} GB")
                print(f"   VRAM reserved: {reserved:.2f} GB\n")
                
        except Exception as e2:
            print(f"   ❌ Also failed: {e2}")
            print(f"\n   Quantization may not be supported for this pipeline.")
            print(f"   Falling back to bfloat16 with full GPU loading...")
            
            try:
                pipe = QwenImageEditPlusPipeline.from_pretrained(
                    base_model_path,
                    torch_dtype=torch.bfloat16
                )
                pipe.to('cuda')
                load_time = time.time() - start
                print(f"   ✅ Model loaded (bfloat16, full GPU) in {load_time:.1f}s\n")
            except torch.cuda.OutOfMemoryError:
                print(f"   ❌ OOM - model too large for GPU")
                print(f"   The GGUF file is ComfyUI-specific and can't be used with diffusers.")
                print(f"   Stick with CPU offloading for now.")
                return 1
    
    print(f"2. Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}\n")
    
    prompt = "Change background to a beach with ocean, keep the person identical"
    print(f"3. Editing with prompt:")
    print(f"   '{prompt}'\n")
    print(f"   Testing inference speed...")
    
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
                generator=torch.manual_seed(42),
            )
        
        result = output.images[0]
        result.save(output_path)
        
        elapsed = time.time() - start
        
        print(f"\n✅ Complete!")
        print(f"   Generation time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        print(f"   Saved to: {output_path}")
        
        print(f"\n" + "=" * 60)
        print("PERFORMANCE COMPARISON")
        print("=" * 60)
        print(f"\nFull bfloat16 model (CPU offload):")
        print(f"  - Generation time: ~420s (7 minutes)")
        print(f"  - VRAM: Offloaded to CPU")
        
        print(f"\nQuantized model:")
        print(f"  - Generation time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            print(f"  - VRAM: {allocated:.2f} GB (on GPU)")
        
        if elapsed < 420:
            speedup = 420 / elapsed
            print(f"\n⚡ Speedup: {speedup:.1f}x faster")
        
        print(f"\nCompare quality:")
        print(f"  - Original (bfloat16): test_data/quick_test.png")
        print(f"  - Quantized: {output_path}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(test_8bit_quantized())
