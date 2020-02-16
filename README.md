[![Docker Build Status](https://img.shields.io/docker/cloud/build/joachimveulemans/license-plate-reader)](https://hub.docker.com/r/joachimveulemans/license-plate-reader/builds)
[![Docker Automated Status](https://img.shields.io/docker/cloud/automated/joachimveulemans/license-plate-reader)](https://hub.docker.com/r/joachimveulemans/license-plate-reader)

# License Plate Reader

## Introduction

This repository contains a Python script that returns the license plate in plain text from a given image or RTSP stream.

## Running the project locally

If you want to run the project locally on your own computer, you can do so in two ways. You can run it like in production and start the Docker container or run it like you would when developing.

### Production-like

Here is assumed that you have [Docker](https://www.docker.com/get-started) installed correctly.

Start of by building the images: `.\00_build_image.cmd` or `./00_build_image.sh`. Alternatively, you can also pull the images that are already build by: `.\00b_pull_image.cmd` or `./00b_pull_image.sh`.

#### Execution

Start reader by: `.\01_start_container.cmd` or `./01_start_container.sh`.

### Development

Here is assumed that you have [Python 3](https://www.python.org/downloads/) installed correctly.

#### Execution

1. Go the the app directory by: `cd app`.
2. Install system dependencies by: `sudo apt install tesseract-ocr`.
3. Install Python dependencies by: `pip3 install -r requirements.txt`.
4. Run the project by: `python3 LicensePlateReader.py`.

## License

Some parts are forked from [sergiomsilva/alpr-unconstrained](https://github.com/sergiomsilva/alpr-unconstrained).