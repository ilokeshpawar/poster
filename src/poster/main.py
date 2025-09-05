import os
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from rich import print

from poster._config import config
from poster._constants import LOGO_SIZE
from poster._helper import remove_image_metadata, rgb_to_hex, svg_to_png

images: dict[str, list] = config["picture"]
logo_s: dict = config["logo"]
fonts: dict = config["fonts"]


def profile():
    # TODO - Implement this later
    pass


def size_matters() -> None:
    """Return the dimensions (width, height) of the image at the given path."""
    for image in images.keys():
        image_path = images[image][0]
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                print(f"Dimensions of {image} ({image_path}): {width}x{height}")
        except UnidentifiedImageError:
            print(f"Skipping non-image file: {image_path}")


def cover_picture(size: Tuple[int, int], greyscale: bool = False) -> Image.Image:
    """Create a new blank image with the given width, height, and background color."""
    bg_color: tuple[int, int, int] = tuple(config["background_color"])

    image = Image.new("RGB", size=size, color=bg_color)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fonts["path"], size=20)
    header_fields = [("prompt", 10), ("name", 40), ("designation", 70)]

    for field, y in header_fields:
        draw.text((50, y), config.get(field, ""), fill=fonts["color"], font=font)
    for logo in logo_s.keys():
        username = logo_s[logo]["username"]
        try:
            svg_to_png(
                svg=Path(f"{logo_s[logo]['path']}".split(".")[0] + ".svg"),
                png=Path(logo_s[logo]["path"]),
                size=LOGO_SIZE,
                background_color=rgb_to_hex(bg_color),
            )
        except Exception:
            continue
        with Image.open(f"{logo_s[logo]['path']}") as _logo:
            image.paste(
                _logo,
                (
                    logo_s[logo]["horizontal_offset"],
                    logo_s[logo]["vertical_offset"],
                ),
            )
        draw.text(
            (
                logo_s[logo]["horizontal_offset"] + LOGO_SIZE[0] + 10,
                logo_s[logo]["vertical_offset"],
            ),
            f"{username}",
            fill=fonts["color"],
            font=font,
        )

    for _image in images.keys():
        image_info = images[_image]
        path = image_info[0]
        box: tuple = tuple(image_info[1])
        new_height = image_info[2]
        try:
            remove_image_metadata(Path(path))
        except Exception as e:
            print(f"Skipping metadata removal for {path}: {e}")
        with Image.open(path) as picture:
            if greyscale:
                picture = picture.convert("L")  # Convert to grayscale
            aspect_ratio = picture.size[0] / picture.size[1]
            new_width = int(new_height * aspect_ratio)
            print(f"Resizing {_image} to {new_width}x{new_height}")
            picture = picture.resize((new_width, new_height))
            image.paste(picture, box)
            used_width = box[0] + new_width
            if used_width > (1400 - 10):  # 10px padding on right
                raise ValueError(
                    f"{chr(0x26A0)} Exceeding the available width by {used_width - (1400 - 10)}px.\
                    I have warned you before, do not commit crime in this image-nary land.{chr(0x1F4A3)}{chr(0x1F4A5)}.\
                    You are trespassing the aspect ratio of 4:1.\
                    Reduce the width of images or number of images or change the horizontal offset.{chr(0x26A0)}"
                )
    for png in os.listdir("assets/svg"):
        if png.endswith(".png"):
            os.unlink(os.path.join("assets/svg", png))
    return image
