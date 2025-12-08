#!/usr/bin/env python3
"""
Generate caption files for FLUX LoRA training.
Creates .txt files with instance prompt for each training image.
"""

from pathlib import Path

def create_captions():
    training_dir = Path("test_data/enriched/v1/test_01_training")
    
    # FLUX LoRA caption format
    # Instance token: "sks" is standard placeholder for the character
    instance_prompt = "a photo of sks person"
    
    print("Creating caption files for FLUX LoRA training...")
    print(f"Training directory: {training_dir}")
    print(f"Instance prompt: '{instance_prompt}'")
    print()
    
    # Find all PNG files
    image_files = sorted(training_dir.glob("*.png"))
    
    if not image_files:
        print(f"❌ No PNG files found in {training_dir}")
        return
    
    print(f"Found {len(image_files)} images")
    print()
    
    # Create caption file for each image
    created_count = 0
    for img_path in image_files:
        caption_path = img_path.with_suffix('.txt')
        
        # Write caption
        caption_path.write_text(instance_prompt)
        created_count += 1
        
        print(f"✅ {img_path.name} → {caption_path.name}")
    
    print()
    print(f"✅ Created {created_count} caption files")
    print()
    print("Next steps:")
    print("1. Review captions (all should say 'a photo of sks person')")
    print("2. Configure ai-toolkit YAML for FLUX LoRA training")
    print("3. Train with: python -m ai_toolkit.run config.yaml")

if __name__ == "__main__":
    create_captions()
