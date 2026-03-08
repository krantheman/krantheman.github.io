#!/usr/bin/env python3
"""
Compress AVIF images to meet size requirements:
- Thumbnails (00.avif): < 150KB
- Other images: < 1MB
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip3 install pillow pillow-avif-plugin")
    exit(1)

# Size limits
THUMBNAIL_MAX = 150 * 1024  # 150KB
IMAGE_MAX = 1024 * 1024  # 1MB


def get_file_size(filepath):
    """Get file size in bytes."""
    return os.path.getsize(filepath)


def format_size(size_bytes):
    """Format bytes to human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f}MB"


def compress_image(filepath, target_size, dry_run=False):
    """
    Compress an AVIF image to meet target size.
    Returns True if compression was successful or needed.
    """
    current_size = get_file_size(filepath)
    if current_size <= target_size:
        return False  # Already meets requirement

    print(f"\nCompressing: {filepath}")
    print(
        f"  Current: {format_size(current_size)} -> Target: {format_size(target_size)}"
    )

    if dry_run:
        print("  [DRY RUN] Would compress this file")
        return True

    # Try different quality levels (start high to preserve quality)
    img = Image.open(filepath)
    quality_levels = [90, 80, 70, 60, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

    for quality in quality_levels:
        # Save to temporary location
        temp_path = str(filepath) + ".temp"
        img.save(temp_path, format="AVIF", quality=quality)

        new_size = get_file_size(temp_path)
        print(f"  Quality {quality}: {format_size(new_size)}", end="")

        if new_size <= target_size:
            # Success! Replace original
            os.replace(temp_path, filepath)
            print(f" ✓ Success!")
            return True
        else:
            print(" (still too large)")
            os.remove(temp_path)

    print("  ✗ Could not compress below target size")
    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Compress oversized AVIF images")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be compressed without actually doing it",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compress all images, not just oversized ones",
    )
    args = parser.parse_args()

    workspace_root = Path(__file__).parent.parent
    image_dirs = [
        workspace_root / "public" / "images",
        workspace_root / "src" / "assets" / "images",
    ]

    thumbnail_count = 0
    thumbnail_compressed = 0
    image_count = 0
    image_compressed = 0

    print("=" * 60)
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    print("=" * 60)

    # Process thumbnails (00.avif files)
    print("\n### Processing thumbnails (00.avif) ###")
    for image_dir in image_dirs:
        if not image_dir.exists():
            continue

        for avif_file in sorted(image_dir.rglob("00.avif")):
            thumbnail_count += 1
            if compress_image(avif_file, THUMBNAIL_MAX, args.dry_run):
                thumbnail_compressed += 1

    # Process other images
    print("\n### Processing other images ###")
    for image_dir in image_dirs:
        if not image_dir.exists():
            continue

        for avif_file in sorted(image_dir.rglob("*.avif")):
            # Skip thumbnails (already processed)
            if avif_file.name == "00.avif":
                continue

            image_count += 1
            if compress_image(avif_file, IMAGE_MAX, args.dry_run):
                image_compressed += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    action = "need compression" if args.dry_run else "compressed"
    print(f"Thumbnails: {thumbnail_compressed}/{thumbnail_count} {action}")
    print(f"Other images: {image_compressed}/{image_count} {action}")
    print(
        f"Total: {thumbnail_compressed + image_compressed}/{thumbnail_count + image_count} {action}"
    )


if __name__ == "__main__":
    main()
