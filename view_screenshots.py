#!/usr/bin/env python3
"""Examine the screenshot images to see desired graph format"""

from PIL import Image
import os

script_dir = "scripts"
images = [
    "Screenshot_2026-02-04-23-06-11-277_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-06-50-790_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-09-40-660_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-09-55-792_com.xm.webapp.jpg"
]

print("="*70)
print("EXAMINING REFERENCE IMAGES FOR GRAPH FORMATTING")
print("="*70)

for i, img_name in enumerate(images, 1):
    img_path = os.path.join(script_dir, img_name)
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            print(f"\n🖼️  Image {i}: {img_name}")
            print(f"   Size: {img.width}x{img.height}px")
            print(f"   Format: {img.format}")
            print(f"   ✅ File exists and is readable")
            # Save a thumbnail for preview
            thumb_path = os.path.join(script_dir, f"thumb_{i}.png")
            img.thumbnail((400, 300))
            img.save(thumb_path)
            print(f"   Thumbnail saved: {thumb_path}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"\n❌ Image {i}: {img_name} - NOT FOUND")

print("\n" + "="*70)
print("To see the images, open them in your file explorer or image viewer")
print("Location: scripts/Screenshot_*.jpg")
print("="*70)
