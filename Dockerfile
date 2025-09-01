FROM ghcr.io/astral-sh/uv:debian-slim

# Metadata
LABEL name="lokesh" \
      email="ilokeshpawar@gmail.com" \
      version="1.0" \
      description="A simple docker image with python 3.13 and a few dependencies installed."

# Install dependencies
RUN apt update && \
    apt install -y --no-install-recommends curl inkscape && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.13
RUN uv python install 3.13 --default

COPY . ./poster/

# Set working directory
WORKDIR /poster
RUN uv sync

CMD ["uv", "run", "poster", "cover", "--background-color", "white"]
