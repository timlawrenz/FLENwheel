#!/usr/bin/env python3
"""
Basic test script to verify Qwen-Image-Edit-2509 loads correctly.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
import time

def main():
    print("=" * 60)
    print("Qwen-Image-Edit-2509 Basic Load Test")
    print("=" * 60)
    
    model_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509"
    
    print(f"\n1. Loading model from: {model_path}")
    print(f"   PyTorch version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA device: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    start = time.time()
    
    try:
        # Enable memory efficient loading with CPU offloading
        pipe = QwenImageEditPlusPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16
        )
        # Use enable_model_cpu_offload for large models
        pipe.enable_model_cpu_offload()
        load_time = time.time() - start
        
        print(f"\n✅ Model loaded successfully in {load_time:.1f}s")
        print(f"\n2. Pipeline components:")
        for name, component in pipe.components.items():
            if component is not None:
                print(f"   - {name}: {type(component).__name__}")
        
        print(f"\n3. Memory usage:")
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"   - Allocated: {allocated:.2f} GB")
            print(f"   - Reserved: {reserved:.2f} GB")
        
        print(f"\n✅ Test passed! Model is ready to use.")
        
    except Exception as e:
        print(f"\n❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
