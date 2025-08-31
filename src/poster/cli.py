from typer import Typer

from poster.constants import LINKEDIN_COVER_SIZE, LINKEDIN_COVER_FILE_NAME
from poster.main import new_image

app = Typer(no_args_is_help=True)


@app.command(no_args_is_help=True)
def cover(background_color: str = "white"):
    """Create a LinkedIn cover image with the specified information."""
    image = new_image(size=LINKEDIN_COVER_SIZE, color=background_color)
    image.save(LINKEDIN_COVER_FILE_NAME)
    print("LinkedIn cover image created")


@app.callback()
def main():
    """Poster CLI - A tool to create social media profile images."""
    pass
