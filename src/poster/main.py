from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from rich import print

from poster._constants import LOGO_SIZE
from poster._helper import load_config, remove_image_metadata, rgb_to_hex, svg_to_png


def profile():
    # TODO - Implement this later
    pass


def size_matters(config_path: Path) -> None:
    """Return the dimensions (width, height) of the image at the given path."""
    config = load_config(config_path)
    images: dict[str, list] = config["picture"]
    for image in images.keys():
        image_path = images[image][0]
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                print(f"Dimensions of {image} ({image_path}): {width}x{height}")
        except UnidentifiedImageError:
            print(f"Skipping non-image file: {image_path}")


def cover_picture(
    config_path: Path,
    size: Tuple[int, int],
    greyscale: bool = False,
    exif_removal: bool = True,
    svg_to_png_conversion: bool = True,
) -> Image.Image:
    config = load_config(config_path)
    images: dict[str, list] = config["picture"]
    logo_s: dict = config["logo"]
    fonts: dict = config["fonts"]
    """Create a new blank image with the given width, height, and background color."""
    bg_color = config["background_color"]
    bg_cover: tuple[int, int, int] = tuple(bg_color["cover"])
    bg_logo: tuple[int, int, int] = tuple(bg_color["logo"])

    image = Image.new("RGB", size=size, color=bg_cover)

    draw = ImageDraw.Draw(image)
    if fonts["path"] != "":
        font = ImageFont.truetype(fonts["path"], size=fonts["size"])
    else:
        font = ImageFont.load_default(size=fonts["size"])
    header_fields = [("prompt", 10), ("name", 40), ("designation", 70)]

    for field, y in header_fields:
        draw.text((50, y), config.get(field, ""), fill=fonts["color"], font=font)
    for logo in logo_s.keys():
        username: str = logo_s[logo]["username"]
        if svg_to_png_conversion:
            svg_to_png(
                svg=Path(f"{logo_s[logo]['path']}".split(".")[0] + ".svg"),
                png=Path(logo_s[logo]["path"]),
                size=LOGO_SIZE,
                background_color=rgb_to_hex(bg_logo),
            )
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
        if exif_removal:
            remove_image_metadata(Path(path))
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
    return image
