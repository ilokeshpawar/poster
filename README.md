
# Poster

- [Poster](#poster)
  - [Introduction](#introduction)
  - [Notes](#notes)
  - [Usage](#usage)
  - [Result](#result)
  - [References](#references)
  - [Contact](#contact)

## Introduction

This repository helps you create a profile picture and cover photo. Inspired by the cover photo shown in [Magical shell history with rust | FOSDEM 2023](https://www.youtube.com/watch?v=uyRmV19qJ2o), I decided to design something similar for myself. The presenter, [Ellie](https://github.com/ellie), is the creator of the shell history management tool [atuin](https://atuin.sh/).

>[!NOTE]
>
> 1. Download [config.toml](./config.toml) and adjust its settings as needed. To prevent runtime errors, either use an absolute path or ensure referenced assets are correctly specified relative to `config.toml`.
> 2. The LinkedIn cover photo size is set to **`1400 x 350 pixels`**, which differs slightly from the recommended size in [Image specifications for LinkedIn](https://www.linkedin.com/help/linkedin/answer/a563309/image-specifications-for-your-linkedin-pages-and-career-pages?lang=en): ***1128 x 376 pixels***.
>

>[!WARNING]
>:bomb: Altering an image's aspect ratio is a cardinal sin in an `image-nary world`. Please avoid this at all costs. :bomb:

## Notes

- All configuration is managed in the [config.toml](./config.toml) file. Please update it according to your requirements.
- For SVG to PNG logo conversion, I used [Inkscape](https://inkscape.org/). If you don't have it installed, simply specify the logo image paths in [config.toml](./config.toml).
- Installing [ExifTool by Phil Harvey](https://exiftool.org/) is optional. You can remove EXIF metadata if you wish, but after cover creation, EXIF data is discarded. Unless you are publishing actual images in a public repository, this is generally not a concern.
- My workflow is Linux-based; I have not tested this on Windows or macOS. If you encounter any issues, feel free to open an issue. It should work fine on Unix-based systems.
- *Please take utmost care regarding privacy. I have only shared information here that is already publicly available. I have avoided sharing unnecessary personal details.*

## Usage

1. Clone the repository:

   ```bash
   git clone git@github.com:ilokeshpawar/poster.git
   cd poster
   ```

2. This project uses [uv](https://docs.astral.sh/uv/) for environment management. Install it from [installation](https://docs.astral.sh/uv/getting-started/installation/).
3. Inside the project directory, install dependencies:

   ```bash
   uv sync
   ```

4. To create the cover photo, run:

   ```bash
   uv run poster --help
   ```

## Result

Explore more examples in the [output directory](./assets/output/). Here is a sample result:
![Alt text](./assets/output/white_bg_greyscale_example.png)

## References

- [YouTube Video](https://www.youtube.com/watch?v=uyRmV19qJ2o)
- [Ellie's GitHub](https://github.com/ellie)
- [atuin](https://atuin.sh/)
- [Personalizing your GitHub profile](https://docs.github.com/en/account-and-profile/get-started/personalizing-your-profile)
- [Image specifications for LinkedIn](https://www.linkedin.com/help/linkedin/answer/a563309/image-specifications-for-your-linkedin-pages-and-career-pages?lang=en)
- [SVG source](https://www.svgrepo.com/)
- [Fonts source](https://fonts.google.com/noto/specimen/Noto+Sans+Mono)
- [Tom's Obvious, Minimal Language (TOML) for config](https://toml.io/en/)
- [ExifTool by Phil Harvey](https://exiftool.org/) was used to remove image metadata. **If you haven't tried it, I highly recommend adding it to your toolkit.**

## Contact

If you have any questions, feel free to reach out via [Gmail](mailto:ilokeshpawar@gmail.com). I'm happy to help.
