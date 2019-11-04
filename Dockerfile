# Define base image
FROM ubuntu:18.04

# Upgrade all existing packages
RUN set -x \
        && apt-get update \
        && apt-get upgrade -y

# Install video packages
RUN apt-get install -y xserver-xorg-video-all libgl1-mesa-glx libgl1-mesa-dri

# Add some packages we need later on
RUN apt-get install -y apt-transport-https ca-certificates git vim sudo htop curl wget mesa-utils python-pip \
    && apt-get install -y software-properties-common libnss3 dirmngr gnupg2 lsb-release tmux apt-utils

# Install some packages because of errors
# https://github.com/NVIDIA/nvidia-docker/issues/864
RUN apt-get install -y libsm6 libxext6 libxrender-dev

# Install project packages
RUN apt-get install -y tesseract-ocr
RUN pip install numpy imutils pytesseract opencv-python scipy

# Set to require no password when executing via sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Copy project contents to home directory
RUN mkdir /home/license
COPY . /home/license

RUN chmod +x /home/license/LicensePlateReader.py

# Finish docker container
STOPSIGNAL SIGTERM
ENTRYPOINT [ "python2.7" ]
CMD [ "/home/license/LicensePlateReader.py" ]
