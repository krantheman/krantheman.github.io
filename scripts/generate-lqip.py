#!/usr/bin/env python3
"""
Generate Low Quality Image Placeholders (LQIP) for all images.
Creates tiny 20x20px versions encoded as base64 data URIs.
"""

import os
import json
import base64
from pathlib import Path
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip3 install pillow pillow-avif-plugin")
    exit(1)


def generate_lqip(image_path, size=64):
    """
    Generate a tiny placeholder for an image.
    Returns base64 encoded data URI.
    """
    try:
        img = Image.open(image_path)

        # Get original dimensions for aspect ratio
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height

        # Calculate placeholder dimensions maintaining aspect ratio
        # Use round() instead of int() for better precision
        if aspect_ratio > 1:
            # Landscape
            placeholder_width = size
            placeholder_height = round(size / aspect_ratio)
        else:
            # Portrait or square
            placeholder_height = size
            placeholder_width = round(size * aspect_ratio)

        # Ensure minimum 1px dimensions
        placeholder_width = max(1, placeholder_width)
        placeholder_height = max(1, placeholder_height)

        # Resize to tiny version with high-quality downsampling
        img_small = img.resize(
            (placeholder_width, placeholder_height), Image.Resampling.LANCZOS
        )

        # Save to bytes buffer as JPEG (smaller than PNG for photos)
        buffer = BytesIO()
        img_small.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
        buffer.seek(0)

        # Encode as base64
        encoded = base64.b64encode(buffer.read()).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{encoded}"

        return {
            "placeholder": data_uri,
            "width": original_width,
            "height": original_height,
        }
    except Exception as e:
        print(f"  Error processing {image_path}: {e}")
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate LQIP for all images")
    parser.add_argument(
        "--size",
        type=int,
        default=64,
        help="Size of the longest edge for LQIP (default: 64px)",
    )
    args = parser.parse_args()

    workspace_root = Path(__file__).parent.parent
    image_dirs = [
        workspace_root / "src" / "assets" / "images",
    ]

    lqip_data = {}
    processed_count = 0

    print(f"Generating LQIP with size={args.size}px (improved precision)...\n")

    for image_dir in image_dirs:
        if not image_dir.exists():
            continue

        for image_path in image_dir.rglob("*.avif"):
            # Get relative path from workspace root
            relative_path = str(image_path.relative_to(workspace_root))

            print(f"Processing: {relative_path}")
            lqip = generate_lqip(image_path, args.size)

            if lqip:
                lqip_data[relative_path] = lqip
                processed_count += 1

        # Also process jpg/jpeg for the home page image
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            for image_path in image_dir.rglob(ext):
                relative_path = str(image_path.relative_to(workspace_root))
                print(f"Processing: {relative_path}")
                lqip = generate_lqip(image_path, args.size)

                if lqip:
                    lqip_data[relative_path] = lqip
                    processed_count += 1

    # Save to JSON file
    output_path = workspace_root / "src" / "lqip-data.json"
    with open(output_path, "w") as f:
        json.dump(lqip_data, f, indent=2)

    print(f"\n✓ Generated LQIP for {processed_count} images")
    print(f"  Output: {output_path}")

    # Show size of generated file
    output_size = os.path.getsize(output_path)
    print(f"  Size: {output_size / 1024:.1f}KB")


if __name__ == "__main__":
    main()
