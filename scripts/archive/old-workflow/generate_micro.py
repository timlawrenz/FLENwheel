#!/usr/bin/env python3
"""
Generate micro-adjustment variations - tiny head/face movements.
Ultra-subtle changes (1-2 degrees) to create in-between states.
Perfect for FLUX LoRA to learn smooth transitions.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from dfloat11 import DFloat11Model
from PIL import Image
import time
from pathlib import Path
from datetime import datetime

def generate_micro_adjustments():
    print("=" * 80)
    print("MICRO-ADJUSTMENTS - Ultra-Subtle Variations")
    print("=" * 80)
    
    # Paths
    base_model = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model = "DFloat11/Qwen-Image-Edit-2509-DF11"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(f"/home/tim/source/activity/FLENwheel/test_data/enriched/v1/batch_{timestamp}_micro")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # MICRO adjustments - barely perceptible changes
    prompts = [
        # Tiny head tilts (1-2 degrees)
        ("tilt_left_tiny", "Tilt the head one degree to the left, preserve the person's identity"),
        ("tilt_right_tiny", "Tilt the head one degree to the right, preserve the person's identity"),
        ("tilt_up_tiny", "Tilt the head one degree upward, preserve the person's identity"),
        ("tilt_down_tiny", "Tilt the head one degree downward, preserve the person's identity"),
        
        # Micro head turns (barely noticeable)
        ("turn_left_micro", "Turn the head very slightly to the left, almost imperceptibly, preserve identity"),
        ("turn_right_micro", "Turn the head very slightly to the right, almost imperceptibly, preserve identity"),
        
        # Chin micro-adjustments
        ("chin_up_micro", "Lift the chin up by one degree, preserve the person's identity"),
        ("chin_down_micro", "Lower the chin down by one degree, preserve the person's identity"),
        
        # Slight weight shifts (asymmetry)
        ("lean_left_subtle", "Make the person lean very subtly to the left, preserve identity"),
        ("lean_right_subtle", "Make the person lean very subtly to the right, preserve identity"),
        
        # Micro facial muscle changes
        ("eyebrow_raise_micro", "Raise one eyebrow very slightly, preserve the person's identity"),
        ("eyebrow_furrow_micro", "Furrow the brow very slightly, preserve the person's identity"),
        
        # Breathing/relaxation micro-states
        ("inhale_subtle", "Show the person in a subtle inhaling state, preserve identity"),
        ("exhale_relaxed", "Show the person in a relaxed exhaling state, preserve identity"),
        
        # Micro-smile variations
        ("smile_beginning", "Show the very beginning of a smile forming, preserve the person's identity"),
        ("smile_ending", "Show a smile just fading, preserve the person's identity"),
    ]
    
    # Create README
    readme_content = f"""# Batch: Micro-Adjustments (Ultra-Subtle)
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Generation Parameters
- **Source Image**: test_01.png
- **Model**: Qwen-Image-Edit-2509 with DFloat11 compression
- **LoRA**: None (base model only)
- **Method**: Micro-adjustments (1-2 degree changes, barely perceptible)
- **Goal**: In-between states for smooth FLUX LoRA learning
- **Inference Steps**: 40
- **Seed**: 42 + image_index (varied per image)

## Strategy: Ultra-Subtle "In-Between" States
These are the **smallest possible variations** - barely noticeable to the eye:
- 1-2 degree head tilts
- Micro facial muscle movements
- Beginning/ending of expressions
- Subtle weight shifts
- Breathing states

## Why This Works
1. **Smooth transitions**: FLUX LoRA learns gradual changes, not just extremes
2. **Natural states**: Captures momentary micro-expressions
3. **Robust identity**: Tiny changes = zero risk of distortion
4. **Data density**: Fills gaps between larger variations

## Prompts Used ({len(prompts)} variations)

### Micro Head Tilts (4)
- tilt_left_tiny: 1° left
- tilt_right_tiny: 1° right
- tilt_up_tiny: 1° up
- tilt_down_tiny: 1° down

### Micro Head Turns (2)
- turn_left_micro: Barely noticeable left turn
- turn_right_micro: Barely noticeable right turn

### Chin Adjustments (2)
- chin_up_micro: 1° chin lift
- chin_down_micro: 1° chin lower

### Weight Shifts (2)
- lean_left_subtle: Subtle left lean
- lean_right_subtle: Subtle right lean

### Facial Muscles (2)
- eyebrow_raise_micro: Slight eyebrow raise
- eyebrow_furrow_micro: Slight brow furrow

### Breathing States (2)
- inhale_subtle: Subtle inhale
- exhale_relaxed: Relaxed exhale

### Smile Transitions (2)
- smile_beginning: Smile starting
- smile_ending: Smile fading

## Quality Criteria
These should be **almost identical** to the source:
- ✅ Changes are subtle and natural
- ✅ Identity perfectly preserved
- ✅ Barely perceptible differences
- ✅ Look like natural micro-moments

Reject if:
- ❌ Changes are too obvious
- ❌ Any identity drift
- ❌ Looks artificial

## Decision
- [ ] Accept for training dataset
- [ ] Needs review
- [ ] Reject (reason: ________________)
"""
    
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created batch folder: {output_dir.name}")
    print(f"✅ Created README: {readme_path}")
    
    print(f"\n📋 Generation Plan:")
    print(f"   Source: test_01.png")
    print(f"   Total variations: {len(prompts)}")
    print(f"   Focus: Micro-adjustments (1-2° changes)")
    print(f"   Method: DFloat11 (no LoRA complexity)")
    print(f"   Estimated time: ~{len(prompts) * 3.8:.0f} minutes ({len(prompts) * 3.8 / 60:.1f} hours)")
    
    proceed = input(f"\n⏱️  This will take ~{len(prompts) * 3.8 / 60:.1f} hours. Proceed? (y/n): ")
    if proceed.lower() != 'y':
        print("Aborted.")
        return
    
    print(f"\n" + "=" * 80)
    print("Loading Model (DFloat11)")
    print("=" * 80)
    
    start = time.time()
    
    # Load pipeline with DFloat11
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
    print(f"✅ Model loaded in {load_time:.1f}s\n")
    
    # Load source image
    source_image = Image.open(source_path)
    print(f"✅ Source image loaded: {source_path}")
    print(f"   Size: {source_image.size}\n")
    
    # Generate variations
    results = []
    
    for idx, (name, prompt) in enumerate(prompts, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(prompts)}] {name}")
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
    
    print(f"\n✅ Successful: {successful}/{len(prompts)}")
    print(f"⏱️  Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"📁 Output: {output_dir}")
    
    print(f"\n📊 Complete Dataset Status:")
    print(f"   Scenes: 20 images")
    print(f"   Gaze: 15 images")
    print(f"   Micro: {successful} images")
    print(f"   Earlier: 8 images")
    print(f"   Total: ~{20 + 15 + successful + 8} images")
    print(f"   ✅ Excellent diversity for FLUX LoRA training!")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Review micro-adjustments (should be barely noticeable)")
    print(f"   2. Count total good images across ALL batches")
    print(f"   3. Organize into training dataset")
    print(f"   4. Ready for FLUX LoRA v1 training!")
    print()

if __name__ == "__main__":
    generate_micro_adjustments()
