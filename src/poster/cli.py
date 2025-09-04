import typer
from typing_extensions import Annotated

from poster.constants import (
    LINKEDIN_COVER_FILE_PATH,
    LINKEDIN_COVER_SIZE,
)
from poster.main import know_the_size, new_image

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
    image = new_image(
        size=LINKEDIN_COVER_SIZE,
        greyscale=greyscale,
    )
    if preview:
        image.show()
    else:
        image.save(LINKEDIN_COVER_FILE_PATH)
        print("LinkedIn cover image created")


@app.command(
    no_args_is_help=False,
    epilog="[green bold italic]Tip: Run this command to help configure your config.toml file.[/]",
)
def size():
    """Know the size of an image or all images in a directory."""
    return know_the_size()


@app.callback()
def main():
    """Poster CLI - A tool to create social media profile images."""
    pass
