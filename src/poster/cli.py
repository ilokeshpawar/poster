import typer
from typing_extensions import Annotated

from poster._config import config
from poster._constants import LINKEDIN_COVER_SIZE
from poster.main import cover_picture, size_matters

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(no_args_is_help=False)
def cover(
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
        size=LINKEDIN_COVER_SIZE,
        greyscale=greyscale,
    )
    if preview:
        image.show()
    else:
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
def size():
    """Know the size of an image or all images in a directory."""
    return size_matters()


@app.callback()
def main():
    """Poster CLI - A tool to create social media profile images."""
    pass
