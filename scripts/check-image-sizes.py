#!/usr/bin/env python3

"""Check that image files meet size requirements:
- Thumbnails (00.avif): < 150KB
- Other images: < 1MB
"""

from pathlib import Path

# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color


def format_size(size_bytes):
    """Format file size in KB or MB"""
    size_kb = size_bytes / 1024
    if size_kb > 1024:
        return f"{size_kb / 1024:.2f}MB"
    return f"{size_kb:.1f}KB"


def check_images():
    """Check all AVIF images in the project"""

    # Find all .avif files
    image_paths = []
    for root_dir in ["public/images", "src/assets/images"]:
        root = Path(root_dir)
        if root.exists():
            image_paths.extend(root.rglob("*.avif"))

    thumbnails_over = []
    images_over = []
    all_thumbnails = []
    all_images = []

    # Separate thumbnails from other images
    for img_path in sorted(image_paths):
        size = img_path.stat().st_size

        if img_path.name == "00.avif":
            all_thumbnails.append((img_path, size))
            if size > 150 * 1024:  # 150KB
                thumbnails_over.append((img_path, size))
        else:
            all_images.append((img_path, size))
            if size > 1024 * 1024:  # 1MB
                images_over.append((img_path, size))

    # Print results
    print("=== Thumbnail files (00.avif) - should be < 150KB ===")
    for img_path, size in all_thumbnails:
        status = f"{RED}✗" if size > 150 * 1024 else f"{GREEN}✓"
        print(f"{status} {img_path}: {format_size(size)}{NC}")

    print("\n=== Other image files - should be < 1MB ===")
    for img_path, size in all_images:
        status = f"{RED}✗" if size > 1024 * 1024 else f"{GREEN}✓"
        print(f"{status} {img_path}: {format_size(size)}{NC}")

    # Summary
    print("\n=== Summary ===")
    print(f"Thumbnails checked: {len(all_thumbnails)}")
    print(f"Thumbnails over 150KB: {RED}{len(thumbnails_over)}{NC}")
    print(f"Images checked: {len(all_images)}")
    print(f"Images over 1MB: {RED}{len(images_over)}{NC}")

    if thumbnails_over or images_over:
        print(f"\n{YELLOW}Some images need optimization!{NC}")
        print("To compress AVIF files, install: pip install pillow-avif-plugin")
        return 1
    else:
        print(f"\n{GREEN}All images are within size limits!{NC}")
        return 0


if __name__ == "__main__":
    exit(check_images())
