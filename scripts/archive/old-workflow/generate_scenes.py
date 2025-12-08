#!/usr/bin/env python3
"""
Generate background and lighting variations using DFloat11 (no LoRA, no angle changes).
Simple and reliable - focus on scene diversity for FLUX training dataset.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from dfloat11 import DFloat11Model
from PIL import Image
import time
from pathlib import Path

def generate_scene_variations():
    print("=" * 80)
    print("SCENE VARIATIONS - Backgrounds & Lighting (No Angles)")
    print("=" * 80)
    
    # Paths
    base_model = "Qwen/Qwen-Image-Edit-2509"
    dfloat11_model = "DFloat11/Qwen-Image-Edit-2509-DF11"
    source_path = "/home/tim/source/activity/FLENwheel/test_data/source/test_01.png"
    
    # Create timestamped output directory
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(f"/home/tim/source/activity/FLENwheel/test_data/enriched/v1/batch_{timestamp}_scenes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create README for this batch
    readme_content = f"""# Batch: Scene Variations
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Generation Parameters
- **Source Image**: test_01.png
- **Model**: Qwen-Image-Edit-2509 with DFloat11 compression
- **LoRA**: None (base model only)
- **Method**: Background and lighting variations only (NO angle changes)
- **Inference Steps**: 40
- **Seed**: 42 + image_index (varied per image)

## Prompts Used
Total: 20 variations focusing on scene diversity

### Outdoor Backgrounds (5)
- forest_day: Forest with trees during daytime
- beach_sunset: Beach at sunset with warm colors
- mountain_view: Mountain landscape view
- city_park: City park with greenery
- garden_flowers: Garden with colorful flowers

### Urban Backgrounds (3)
- urban_street: Modern urban street with buildings
- cafe_outdoor: Outdoor cafe terrace
- city_night: City at night with lights

### Indoor Backgrounds (4)
- studio_white: Clean white photography studio
- home_cozy: Cozy home interior with warm lighting
- office_modern: Modern office interior
- library_books: Library with bookshelves

### Lighting Variations (5)
- natural_light: Natural daylight lighting
- golden_hour: Golden hour warm sunset lighting
- soft_studio: Soft professional studio lighting
- dramatic_side: Dramatic side lighting with shadows
- overcast_soft: Soft overcast lighting

### Seasonal Scenes (3)
- autumn_leaves: Autumn scene with fall leaves
- spring_cherry: Spring cherry blossom scene
- winter_snow: Winter scene with snow

## Quality Notes
(Review and add notes here after manual inspection)

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
    
    # Scene and lighting variations (no angle changes!)
    prompts = [
        # Outdoor backgrounds
        ("forest_day", "Change background to a forest with trees during daytime, preserve the person's identity"),
        ("beach_sunset", "Change background to a beach at sunset with warm colors, preserve the person's identity"),
        ("mountain_view", "Change background to mountain landscape view, preserve the person's identity"),
        ("city_park", "Change background to a city park with greenery, preserve the person's identity"),
        ("garden_flowers", "Change background to a garden with colorful flowers, preserve the person's identity"),
        
        # Urban backgrounds
        ("urban_street", "Change background to modern urban street with buildings, preserve the person's identity"),
        ("cafe_outdoor", "Change background to outdoor cafe terrace, preserve the person's identity"),
        ("city_night", "Change background to city at night with lights, preserve the person's identity"),
        
        # Indoor backgrounds
        ("studio_white", "Change background to clean white photography studio, preserve the person's identity"),
        ("home_cozy", "Change background to cozy home interior with warm lighting, preserve the person's identity"),
        ("office_modern", "Change background to modern office interior, preserve the person's identity"),
        ("library_books", "Change background to library with bookshelves, preserve the person's identity"),
        
        # Lighting variations (same/similar background)
        ("natural_light", "Add natural daylight lighting, preserve the person's identity"),
        ("golden_hour", "Add golden hour warm sunset lighting, preserve the person's identity"),
        ("soft_studio", "Add soft professional studio lighting, preserve the person's identity"),
        ("dramatic_side", "Add dramatic side lighting with shadows, preserve the person's identity"),
        ("overcast_soft", "Add soft overcast lighting, preserve the person's identity"),
        
        # Mixed scenes
        ("autumn_leaves", "Change background to autumn scene with fall leaves, preserve the person's identity"),
        ("spring_cherry", "Change background to spring cherry blossom scene, preserve the person's identity"),
        ("winter_snow", "Change background to winter scene with snow, preserve the person's identity"),
    ]
    
    print(f"\n📋 Generation Plan:")
    print(f"   Source: test_01.png")
    print(f"   Total variations: {len(prompts)}")
    print(f"   Focus: Backgrounds & lighting (NO angle changes)")
    print(f"   Method: DFloat11 (no LoRA complexity)")
    print(f"   Estimated time: ~{len(prompts) * 3.8:.0f} minutes ({len(prompts) * 3.8 / 60:.1f} hours)")
    
    proceed = input(f"\n⏱️  This will take ~{len(prompts) * 3.8 / 60:.1f} hours. Proceed? (y/n): ")
    if proceed.lower() != 'y':
        print("Aborted.")
        return
    
    print(f"\n" + "=" * 80)
    print("Loading Model (DFloat11 - Fast & Reliable)")
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
    
    print(f"\n📊 Dataset Status:")
    print(f"   Current good images: ~8 (from earlier tests)")
    print(f"   New images generated: {successful}")
    print(f"   Total: ~{8 + successful} images")
    if 8 + successful >= 30:
        print(f"   ✅ Ready for FLUX LoRA training! (≥30 images)")
    else:
        print(f"   ⚠️  Need ~{30 - (8 + successful)} more images for training")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Review images in {output_dir}")
    print(f"   2. Move good ones to data/enriched/v1/good/")
    print(f"   3. Count total good images")
    print(f"   4. If ≥30 → Train first FLUX LoRA!")
    print(f"   5. If <30 → Generate a few more variations")
    print()

if __name__ == "__main__":
    generate_scene_variations()
