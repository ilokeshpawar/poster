from pathlib import Path

import typer
from typing_extensions import Annotated

from poster._constants import LINKEDIN_COVER_SIZE
from poster._helper import load_config
from poster.main import cover_picture, size_matters

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(no_args_is_help=False)
def cover(
    config_path: Annotated[
        Path,
        typer.Option("--config", "-c", help="config.toml path"),
    ],
    conversion: Annotated[
        bool,
        typer.Option(
            help="Skip svg to png conversion rather use logo.png provided in config.toml",
        ),
    ] = True,
    exif_removal: Annotated[
        bool,
        typer.Option(help="Skip removing EXIF metadata from pictures"),
    ] = True,
    greyscale: Annotated[
        bool,
        typer.Option(
            "--greyscale", "-g", help="To make the cover greyscale. Default is color."
        ),
    ] = False,
    preview: Annotated[
        bool,
        typer.Option(
            "--preview", "-p", help="To see the preview before saving the actual cover"
        ),
    ] = False,
):
    """Create a LinkedIn cover image with the specified information."""
    image = cover_picture(
        config_path=config_path,
        size=LINKEDIN_COVER_SIZE,
        greyscale=greyscale,
        exif_removal=exif_removal,
        svg_to_png_conversion=conversion,
    )
    if preview:
        image.show()
    else:
        config = load_config(config_path=config_path)
        cover_path = config["cover_output_path"]
        image.save(cover_path)
        print("LinkedIn cover image created")


# @app.command()
# def profile():
#     pass


@app.command(
    no_args_is_help=False,
    epilog="[green bold italic]Tip: Run this command to help configure your config.toml file.[/]",
)
def size(
    config_path: Annotated[
        Path,
        typer.Option("--config", "-c", help="config.toml path"),
    ],
):
    """Know the size of an image or all images in a directory."""
    return size_matters(config_path)


@app.callback()
def main():
    """Poster CLI - A tool to create social media profile images."""
    pass
