import subprocess
from pathlib import Path
from tomllib import load as toml_load
from typing import NewType, Tuple

RgbHex = NewType("RgbHex", str)


def load_config(config_path: Path) -> dict:
    """Load configuration from a TOML file."""
    with config_path.open("rb") as f:
        config = toml_load(f)
    return config


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
            f"Error converting SVG to PNG: {e}.\
            Ensure Inkscape is installed and available in your PATH,\
            or use the `--no-conversion` flag. Alternatively,\
            provide the path for logos to load from."
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
        print(
            f"Failed to remove metadata: {e}.\
            Please ensure exiftool is installed and available in your PATH,\
            or use the `--no-exif-removal` flag."
        )
        raise
