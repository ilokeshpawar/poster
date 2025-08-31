import os
import subprocess
from pathlib import Path
from tomllib import load as toml_load
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from rich import print

from poster.constants import LOGO_SIZE


def load_config(config_path: Path) -> dict:
    """Load configuration from a TOML file."""
    with config_path.open("rb") as f:
        config = toml_load(f)
    return config


def svg_to_png(
    svg_path: Path, png_path: Path, size: Tuple[int, int], background_color: str
) -> None:
    """Convert an SVG file to a PNG file with the specified size."""
    try:
        subprocess.run(
            [
                "inkscape",
                svg_path,
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={size[0]}",
                f"--export-height={size[1]}",
                f"--export-background={background_color}",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error converting SVG to PNG: {e}")
        raise


def new_image(size: Tuple[int, int], color: str = "white") -> Image.Image:
    """Create a new blank image with the given width, height, and background color."""
    config = load_config(Path("config/config.toml"))

    image = Image.new("RGB", size=size, color=color)
    logo_info = config["logo"]

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(config["fonts"]["path"], size=20)
    header_fields = [("prompt", 10), ("name", 40), ("designation", 70)]

    for field, y in header_fields:
        draw.text((50, y), config.get(field, ""), fill="black", font=font)
    for logo in logo_info.keys():
        username = logo_info[logo]["username"]
        svg_to_png(
            svg_path=Path(f"{logo_info[logo]['path']}".split(".")[0] + ".svg"),
            png_path=Path(logo_info[logo]["path"]),
            size=LOGO_SIZE,
            background_color=color,
        )
        with Image.open(f"{logo_info[logo]['path']}") as logo_img:
            image.paste(
                logo_img,
                (
                    logo_info[logo]["horizontal_offset"],
                    logo_info[logo]["vertical_offset"],
                ),
            )
        draw.text(
            (
                logo_info[logo]["horizontal_offset"] + LOGO_SIZE[0] + 10,
                logo_info[logo]["vertical_offset"],
            ),
            f"{username}",
            fill="black",
            font=font,
        )
    for png in os.listdir("assets"):
        if png.endswith(".png"):
            os.unlink(os.path.join("assets", png))
    return image
