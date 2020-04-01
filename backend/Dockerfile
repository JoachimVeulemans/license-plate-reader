# 1 - Define base image
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# 2 - Run apt update
RUN apt-get update && \
    apt-get -y upgrade

# 3 - Install some needed packages
RUN apt-get install -y python3.6 python3-pip gcc wget python-opencv

# 4 - Copy the requirements.txt to Docker container
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# 5 - Install tensorflow - CPU
RUN wget -c -N http://joachimveulemans.be/projects/tensorflow-1.14.1-cp36-cp36m-linux_x86_64.whl
RUN pip3 install tensorflow-1.14.1-cp36-cp36m-linux_x86_64.whl

# 6 - Expose port 443 to bind to later on
EXPOSE 443

# 7 - Download weights
RUN wget -c -N http://joachimveulemans.be/projects/vehicle.weights -P models/
RUN wget -c -N http://joachimveulemans.be/projects/lp.weights -P models/

# 8 - Copy whole project to Docker container
COPY . /app

# 9 - Set environment to use port 443
ENV PORT 443

# 10 - Define the working directory
WORKDIR /app

# 11 - Set entrypoint to Python
ENTRYPOINT [ "python3.6" ]

# 12 - Launch app.py in command line
CMD [ "server.py" ]
