import subprocess
from pathlib import Path
from typing import NewType, Tuple

RgbHex = NewType("RgbHex", str)


def rgb_to_hex(rgb: tuple[int, int, int]) -> RgbHex:
    return RgbHex(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")


def svg_to_png(
    svg: Path, png: Path, size: Tuple[int, int], background_color: RgbHex
) -> None:
    """Convert an SVG file to a PNG file with the specified size."""
    try:
        subprocess.run(
            [
                "inkscape",
                svg,
                "--export-type=png",
                f"--export-filename={png}",
                f"--export-width={size[0]}",
                f"--export-height={size[1]}",
                f"--export-background={background_color}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"Error converting SVG to PNG: {e}. Make sure you have inkscape installed\
                and in your path or use `--skip-conversion` flag and\
                      make sure to put {'logo'}.png with in `asset/svg/ directory.`"
        )
        raise


def remove_image_metadata(image: Path) -> None:
    """Remove metadata from an image file using exiftool."""
    try:
        subprocess.run(
            [
                "exiftool",
                "-all=",
                "-overwrite_original",
                str(image),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error removing metadata: {e}")
        raise
