#!/usr/bin/env python3
"""
Quick source image assessment for angle diversity
"""

from pathlib import Path
import sys

SOURCE_DIR = Path.home() / "source/activity/FLENwheel/data/0I1/source"

def assess_sources():
    images = sorted(SOURCE_DIR.glob("*.*"))
    
    print("=" * 70)
    print("0I1 Source Image Assessment")
    print("=" * 70)
    print(f"\n📁 Location: {SOURCE_DIR}")
    print(f"📊 Total images: {len(images)}\n")
    
    print("🖼️  Image List:")
    print("-" * 70)
    for i, img in enumerate(images, 1):
        print(f"{i:2d}. {img.name}")
    
    print("\n" + "=" * 70)
    print("📋 MANUAL ASSESSMENT NEEDED")
    print("=" * 70)
    print("""
Open the images and categorize by angle:

Command to view all:
  eog ~/source/activity/FLENwheel/data/0I1/source/*.{jpeg,png}

Then count:
  - Front views (looking at camera, face on)
  - Half-left (3/4 view, slightly turned left)
  - Left profile (side view, facing left)
  - Half-right (3/4 view, slightly turned right)
  - Right profile (side view, facing right)
  - Full-body shots (not just head/shoulders)

Update SOURCE_ASSESSMENT.md with your findings!
    """)
    
    print("=" * 70)

if __name__ == "__main__":
    assess_sources()
