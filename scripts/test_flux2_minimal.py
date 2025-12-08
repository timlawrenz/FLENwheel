#!/usr/bin/env python3
"""
Minimal FLUX2 Pipeline Test with Maximum CPU Offloading
Tests if FLUX2 can run on RTX 4090 with aggressive memory management
"""

import torch
import gc
from diffusers import Flux2Pipeline

def clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def get_vram_gb():
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024**3
    return 0

def main():
    print("Loading FLUX2 with maximum CPU offload...")
    
    clear_memory()
    
    # Use the quantized checkpoint
    pipe = Flux2Pipeline.from_pretrained(
        "black-forest-labs/FLUX.2-dev",
        torch_dtype=torch.bfloat16,
    )
    
    # Enable all memory optimizations
    pipe.enable_model_cpu_offload()
    pipe.enable_sequential_cpu_offload()
    
    print(f"VRAM after loading: {get_vram_gb():.2f}GB")
    
    # Simple test
    print("\nTesting single image generation...")
    image = pipe(
        "a portrait of a person",
        num_inference_steps=4,  # Minimal for testing
        height=512,
        width=512,
    ).images[0]
    
    print(f"VRAM after generation: {get_vram_gb():.2f}GB")
    print("✅ Success!")
    
    image.save("test_output.png")
    print("Saved to test_output.png")

if __name__ == "__main__":
    main()
