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


def remove_image_metadata(image: Path) -> None:
    """Remove metadata from an image file using exiftool."""
    try:
        subprocess.run(
            ["exiftool", "-all=", "-overwrite_original", str(image)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error removing metadata: {e}")
        raise


def new_image(size: Tuple[int, int], color: str = "white") -> Image.Image:
    """Create a new blank image with the given width, height, and background color."""
    config = load_config(Path("config/config.toml"))
    # print(f"config: {config}")  # ANCHOR - Debugging line

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

    pictures = config["picture"]
    horizontal_offset = 480
    for pic in pictures.keys():
        try:
            remove_image_metadata(Path(pictures[pic]))
        except Exception as e:
            print(f"Skipping metadata removal for {pictures[pic]}: {e}")
        with Image.open(pictures[pic]) as pic_img:
            pic_img = pic_img.convert("L")  # Convert to grayscale
            aspect_ratio = pic_img.size[0] / pic_img.size[1]
            if str(pic).startswith("lol"):
                new_height = 330
            else:
                new_height = 165
            new_width = int(new_height * aspect_ratio)
            print(f"Resizing {pic} to {new_width}x{new_height}")
            pic_img = pic_img.resize((new_width, new_height))
            image.paste(
                pic_img,
                (horizontal_offset, 10),
            )
        if str(pic).startswith("lol"):
            horizontal_offset += new_width + 10
        else:
            horizontal_offset += new_width + 10
    for png in os.listdir("assets/svg"):
        if png.endswith(".png"):
            os.unlink(os.path.join("assets/svg", png))
    return image
