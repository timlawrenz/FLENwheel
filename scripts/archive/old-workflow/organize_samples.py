#!/usr/bin/env python3
"""
Organize training samples by checkpoint step for easy comparison
"""

import os
import shutil
from pathlib import Path
import re

SAMPLES_DIR = Path("/mnt/essdee/ai-toolkit/output/test_01_v1/samples")
OUTPUT_DIR = Path.home() / "source/activity/FLENwheel/data/t01p/flux/v1/evaluation"

# Key checkpoints to evaluate
CHECKPOINTS = {
    "000000000": "step_0000_baseline",
    "000000250": "step_0250",
    "000000500": "step_0500",
    "000001000": "step_1000",
    "000001500": "step_1500",
    "000002000": "step_2000",
    "000002500": "step_2500",
    "000002750": "step_2750",
    "000003000": "step_3000_final"
}

# Training prompts (from config)
PROMPT_NAMES = [
    "business_suit",
    "beach_casual",
    "winter_mountain",
    "chef_kitchen",
    "athletic_park",
    "library_reading",
    "music_festival",
    "formal_ballroom"
]

def organize_samples():
    """Copy samples into organized structure"""
    
    # Create checkpoint directories
    for checkpoint_name in CHECKPOINTS.values():
        checkpoint_dir = OUTPUT_DIR / checkpoint_name
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Pattern: timestamp__STEPNUMBER_PROMPTINDEX.jpg
    pattern = re.compile(r'(\d+)__(\d+)_(\d+)\.jpg')
    
    for sample_file in sorted(SAMPLES_DIR.glob("*.jpg")):
        match = pattern.match(sample_file.name)
        if not match:
            continue
        
        timestamp, step_num, prompt_idx = match.groups()
        
        # Find matching checkpoint
        if step_num in CHECKPOINTS:
            checkpoint_name = CHECKPOINTS[step_num]
            prompt_name = PROMPT_NAMES[int(prompt_idx)] if int(prompt_idx) < len(PROMPT_NAMES) else f"prompt_{prompt_idx}"
            
            # Copy with descriptive name
            dest_name = f"{prompt_name}.jpg"
            dest_path = OUTPUT_DIR / checkpoint_name / dest_name
            
            shutil.copy2(sample_file, dest_path)
            print(f"Copied: {checkpoint_name}/{dest_name}")

    print(f"\n✅ Organized samples into {len(CHECKPOINTS)} checkpoint directories")
    print(f"📁 Location: {OUTPUT_DIR}")

if __name__ == "__main__":
    organize_samples()
