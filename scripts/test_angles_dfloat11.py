#!/usr/bin/env python3
"""
Comprehensive angle test with DFloat11 compression and optional LoRA.
Tests both base model and dx8152 LoRA for angle variations.
Total time: ~46 minutes (12 images × 3.8 min each)
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from dfloat11 import DFloat11Model
from PIL import Image
import time
from pathlib import Path

def test_all_angles():
    print("=" * 80)
    print("COMPREHENSIVE ANGLE TEST - DFloat11 + Base Model + LoRA")
    print("=" * 80)
    
    # Paths
    base_model = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model = "DFloat11/Qwen-Image-Edit-2509-DF11"
    lora_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-edit-multiple-angles/镜头转换.safetensors"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    output_dir = Path("/home/tim/source/activity/FLENwheel/test_data")
    
    # Angle test prompts
    angle_tests = [
        ("left_view", "Change camera angle to left side view, keep the person identical"),
        ("right_view", "Change camera angle to right side view, keep the person identical"),
        ("profile_left", "Show profile view from the left side, preserve facial features"),
        ("profile_right", "Show profile view from the right side, preserve facial features"),
        ("higher_angle", "Show from a higher camera angle looking down, keep features identical"),
        ("lower_angle", "Show from a lower camera angle looking up, keep features identical"),
    ]
    
    print(f"\n📋 Test Plan:")
    print(f"   - 6 angle variations")
    print(f"   - 2 models: Base + dx8152 LoRA")
    print(f"   - Total: 12 images")
    print(f"   - Estimated time: ~46 minutes (3.8 min/image)")
    print(f"\n" + "=" * 80)
    
    # Load source image
    print(f"\n📷 Loading source image: {source_path}")
    source_image = Image.open(source_path)
    print(f"   Image size: {source_image.size}")
    
    # ========================================================================
    # TEST 1: BASE MODEL (DFloat11)
    # ========================================================================
    
    print(f"\n" + "=" * 80)
    print("TEST 1: BASE MODEL (DFloat11 Compressed)")
    print("=" * 80)
    
    print(f"\n1. Loading base model with DFloat11...")
    start = time.time()
    
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16
    )
    
    DFloat11Model.from_pretrained(
        dfloat11_model,
        bfloat16_model=pipeline.transformer,
        device="cpu",
        cpu_offload=True,
        cpu_offload_blocks=20,
        pin_memory=True,
    )
    
    pipeline.enable_model_cpu_offload()
    
    load_time = time.time() - start
    print(f"   ✅ Model loaded in {load_time:.1f}s")
    
    # Generate base model variations
    base_results = []
    
    for idx, (name, prompt) in enumerate(angle_tests, 1):
        print(f"\n[{idx}/6] {name}")
        print(f"   Prompt: {prompt}")
        
        output_path = output_dir / f"base_{name}.png"
        
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
            
            print(f"   ✅ Saved: {output_path.name}")
            print(f"   ⏱️  Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
            
            base_results.append({
                "name": name,
                "output": output_path,
                "time": elapsed,
                "success": True
            })
            
        except Exception as e:
            elapsed = time.time() - start
            print(f"   ❌ Error: {e}")
            base_results.append({
                "name": name,
                "output": None,
                "time": elapsed,
                "success": False,
                "error": str(e)
            })
    
    # ========================================================================
    # TEST 2: BASE MODEL + dx8152 LoRA (DFloat11)
    # ========================================================================
    
    print(f"\n" + "=" * 80)
    print("TEST 2: dx8152 LORA (DFloat11 Compressed)")
    print("=" * 80)
    
    print(f"\n2. Loading dx8152 LoRA weights...")
    start = time.time()
    
    try:
        pipeline.load_lora_weights(lora_path)
        lora_time = time.time() - start
        print(f"   ✅ LoRA loaded in {lora_time:.1f}s")
        lora_loaded = True
    except Exception as e:
        print(f"   ❌ Error loading LoRA: {e}")
        print(f"   Continuing with base model only...")
        lora_loaded = False
    
    # Generate LoRA variations (if loaded successfully)
    lora_results = []
    
    if lora_loaded:
        for idx, (name, prompt) in enumerate(angle_tests, 1):
            print(f"\n[{idx}/6] {name} (with LoRA)")
            print(f"   Prompt: {prompt}")
            
            output_path = output_dir / f"lora_{name}.png"
            
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
                
                print(f"   ✅ Saved: {output_path.name}")
                print(f"   ⏱️  Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
                
                lora_results.append({
                    "name": name,
                    "output": output_path,
                    "time": elapsed,
                    "success": True
                })
                
            except Exception as e:
                elapsed = time.time() - start
                print(f"   ❌ Error: {e}")
                lora_results.append({
                    "name": name,
                    "output": None,
                    "time": elapsed,
                    "success": False,
                    "error": str(e)
                })
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print(f"\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    base_successful = sum(1 for r in base_results if r["success"])
    base_time = sum(r["time"] for r in base_results if r["success"])
    
    print(f"\n📊 Base Model Results:")
    print(f"   Successful: {base_successful}/6")
    print(f"   Total time: {base_time:.1f}s ({base_time/60:.1f} min)")
    if base_successful > 0:
        print(f"   Avg time: {base_time/base_successful:.1f}s per image")
    
    if lora_loaded:
        lora_successful = sum(1 for r in lora_results if r["success"])
        lora_time = sum(r["time"] for r in lora_results if r["success"])
        
        print(f"\n📊 LoRA Results:")
        print(f"   Successful: {lora_successful}/6")
        print(f"   Total time: {lora_time:.1f}s ({lora_time/60:.1f} min)")
        if lora_successful > 0:
            print(f"   Avg time: {lora_time/lora_successful:.1f}s per image")
    
    print(f"\n📁 Output Files:")
    print(f"   Base model images: test_data/base_*.png")
    if lora_loaded:
        print(f"   LoRA images: test_data/lora_*.png")
    
    print(f"\n🔍 Compare Results:")
    print(f"   1. Base vs LoRA quality for angle changes")
    print(f"   2. Character identity preservation")
    print(f"   3. Angle change effectiveness")
    
    print(f"\n✅ All tests complete!")
    print("=" * 80)
    print()

if __name__ == "__main__":
    test_all_angles()
