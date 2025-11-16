#!/usr/bin/env python3
"""
Test script for Qwen-Image-Edit with Multiple-angles LoRA
Tests character angle transformation while preserving identity
"""
import torch
from PIL import Image
from pathlib import Path
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image
import sys

def test_basic_transformation(
    image_path: str,
    prompt: str,
    output_path: str,
    model_path: str = "/mnt/essdee/ComfyUI/models/unet/qwen-image-edit",
    lora_path: str = "/mnt/essdee/ComfyUI/models/loras/qwen-image-edit/multiple-angles"
):
    """
    Test basic image transformation with Qwen-Image-Edit + Multiple-angles LoRA
    
    Args:
        image_path: Path to input test image
        prompt: Transformation prompt (e.g., "Rotate camera 45 degrees to the left")
        output_path: Where to save result
        model_path: Path to base Qwen model
        lora_path: Path to Multiple-angles LoRA
    """
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         QWEN-IMAGE-EDIT + MULTIPLE-ANGLES TEST                ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    
    # Check if we have GGUF or safetensors
    gguf_file = Path(model_path) / "Qwen-Image-Edit-2509-Q8_0.gguf"
    
    if gguf_file.exists():
        print("⚠️  GGUF format detected!")
        print("   Standard diffusers doesn't directly support GGUF.")
        print("   We need to either:")
        print("   1. Convert GGUF to safetensors")
        print("   2. Use ComfyUI instead")
        print("   3. Use llama.cpp compatible library")
        print()
        print("   Let's check if we can download the original safetensors version...")
        return None
    
    print(f"📁 Input image: {image_path}")
    print(f"💬 Prompt: {prompt}")
    print(f"📁 Output: {output_path}")
    print()
    
    # Load image
    print("📸 Loading input image...")
    image = load_image(image_path)
    print(f"   Size: {image.size}")
    print()
    
    # Load pipeline
    print("🔧 Loading Qwen-Image-Edit pipeline...")
    print("   (This may take a minute...)")
    
    try:
        pipe = AutoPipelineForImage2Image.from_pretrained(
            "Qwen/Qwen-Image-Edit-2509",
            torch_dtype=torch.float16,
            variant="fp16"
        )
        pipe.to("cuda")
        print("   ✅ Base model loaded!")
    except Exception as e:
        print(f"   ❌ Error loading base model: {e}")
        print("   Trying without variant...")
        pipe = AutoPipelineForImage2Image.from_pretrained(
            "Qwen/Qwen-Image-Edit-2509",
            torch_dtype=torch.float16
        )
        pipe.to("cuda")
    
    # Load LoRA
    print()
    print("🔧 Loading Multiple-angles LoRA...")
    lora_weights = Path(lora_path) / "镜头转换.safetensors"
    
    if lora_weights.exists():
        pipe.load_lora_weights(str(lora_path), weight_name="镜头转换.safetensors")
        print(f"   ✅ LoRA loaded from {lora_weights}")
    else:
        print(f"   ⚠️  LoRA file not found: {lora_weights}")
        print("   Continuing without LoRA...")
    
    # Run transformation
    print()
    print("🎨 Running transformation...")
    print(f"   Prompt: '{prompt}'")
    
    result = pipe(
        prompt=prompt,
        image=image,
        num_inference_steps=20,
        strength=0.8,
        guidance_scale=7.5
    ).images[0]
    
    # Save result
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Transformation complete!")
    print(f"📁 Result saved to: {output_path}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    return result


if __name__ == "__main__":
    # Test configuration
    test_image = "test_data/source/test_01.png"
    test_prompt = "Rotate camera 45 degrees to the left"
    output_file = "test_data/results/loras/test_01_rotated_left.png"
    
    print("Starting basic transformation test...")
    print()
    
    result = test_basic_transformation(
        image_path=test_image,
        prompt=test_prompt,
        output_path=output_file
    )
    
    if result:
        print()
        print("🎉 Test successful!")
        print()
        print("Next steps:")
        print("1. Review output image")
        print("2. Check if character identity is preserved")
        print("3. If successful, test all 5 images")
    else:
        print()
        print("⚠️  Need to address GGUF format issue first")
        print("   Will download safetensors version...")
