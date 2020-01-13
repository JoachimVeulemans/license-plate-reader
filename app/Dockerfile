# Define base image
FROM ubuntu:18.04

# Set to UTF-8 otherwise would get weird errors
ENV LANG C.UTF-8

# Upgrade all existing packages
RUN set -x \
        && apt-get update \
        && apt-get upgrade -y

# Install video packages
RUN apt-get install -y xserver-xorg-video-all libgl1-mesa-glx libgl1-mesa-dri

# Add some packages we need later on
RUN apt-get install -y apt-transport-https ca-certificates git vim sudo htop curl wget mesa-utils python3-pip \
    && apt-get install -y software-properties-common libnss3 dirmngr gnupg2 lsb-release tmux apt-utils

# Install some packages because of errors
# https://github.com/NVIDIA/nvidia-docker/issues/864
RUN apt-get install -y libsm6 libxext6 libxrender-dev

# Install project packages
RUN apt-get install -y tesseract-ocr
COPY requirements.txt /home/license/requirements.txt
RUN pip3 install -r /home/license/requirements.txt

# Set to require no password when executing via sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Copy project contents to home directory
COPY . /home/license

RUN chmod +rwx /home/license/

# Finish docker container
STOPSIGNAL SIGTERM
