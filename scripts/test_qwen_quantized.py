#!/usr/bin/env python3
"""
Test Qwen-Image-Edit-2509 with 8-bit GGUF quantization.
Compare speed vs quality with bfloat16 version.
"""

import torch
from diffusers import QwenImageEditPlusPipeline, GGUFQuantizationConfig
from PIL import Image
import time

def test_quantized():
    print("=" * 60)
    print("Qwen-Image-Edit-2509 8-bit GGUF Quantized Test")
    print("=" * 60)
    
    gguf_file = "/mnt/essdee/ComfyUI/models/unet/qwen-image-edit/Qwen-Image-Edit-2509-Q8_0.gguf"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    output_path = "/home/tim/source/activity/FLENwheel/test_data/quantized_test.png"
    
    print(f"\n1. Loading 8-bit quantized model...")
    print(f"   GGUF file: {gguf_file}")
    print(f"   Size: 21GB (vs 54GB full model)")
    
    start = time.time()
    
    try:
        # Create GGUF quantization config
        quantization_config = GGUFQuantizationConfig(
            compute_dtype=torch.bfloat16,
            file=gguf_file
        )
        
        # Load pipeline with GGUF quantization
        # Note: We might need to load from the original model path
        # and apply quantization, or use a specific loading method
        print(f"\n   Attempting to load with GGUF config...")
        
        pipe = QwenImageEditPlusPipeline.from_pretrained(
            "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509",
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16,
        )
        
        # Try moving to GPU directly (quantized models should fit)
        pipe.to('cuda')
        
        load_time = time.time() - start
        print(f"   ✅ Model loaded in {load_time:.1f}s\n")
        
        # Check VRAM usage
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"   VRAM allocated: {allocated:.2f} GB")
            print(f"   VRAM reserved: {reserved:.2f} GB\n")
        
    except Exception as e:
        print(f"   ❌ Error loading GGUF model: {e}")
        print(f"\n   Trying alternate approach...")
        
        # Alternative: Try loading GGUF file directly
        try:
            # This might require different syntax - GGUF support is new
            pipe = QwenImageEditPlusPipeline.from_single_file(
                gguf_file,
                torch_dtype=torch.bfloat16,
            )
            pipe.to('cuda')
            load_time = time.time() - start
            print(f"   ✅ Model loaded from GGUF in {load_time:.1f}s\n")
        except Exception as e2:
            print(f"   ❌ Also failed: {e2}")
            print(f"\n   The GGUF file might need ComfyUI-specific loading.")
            print(f"   You may need to use ComfyUI's workflow system for GGUF models.")
            return 1
    
    print(f"2. Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}\n")
    
    prompt = "Change background to a beach with ocean, keep the person identical"
    print(f"3. Editing with prompt:")
    print(f"   '{prompt}'\n")
    print(f"   Testing inference speed with quantized model...")
    
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
        print(f"   Generation time: {elapsed:.1f}s")
        print(f"   Saved to: {output_path}")
        
        print(f"\n" + "=" * 60)
        print("PERFORMANCE COMPARISON")
        print("=" * 60)
        print(f"\nFull bfloat16 model (CPU offload):")
        print(f"  - Model size: 54GB")
        print(f"  - Generation time: ~420s (7 minutes)")
        print(f"  - VRAM: Offloaded to CPU")
        
        print(f"\n8-bit GGUF quantized:")
        print(f"  - Model size: 21GB (61% smaller)")
        print(f"  - Generation time: {elapsed:.1f}s")
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            print(f"  - VRAM: {allocated:.2f} GB (fits in GPU!)")
        
        speedup = 420 / elapsed
        print(f"\n⚡ Speedup: {speedup:.1f}x faster")
        
        print(f"\nCompare quality:")
        print(f"  - Original: test_data/quick_test.png")
        print(f"  - Quantized: {output_path}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(test_quantized())
