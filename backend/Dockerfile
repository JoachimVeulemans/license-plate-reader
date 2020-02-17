# 1 - Define base image
FROM python:3.6

# 2 - Run apt update
RUN apt-get update

# 3 - Install some needed packages
RUN apt-get install -y python3-dev gcc

# 4 - Copy the requirements.txt to Docker container
COPY requirements.txt requirements.txt

# 5 - Install some needed packages for the project
RUN pip install -r requirements.txt

# 6 - Expose port 443 to bind to later on
EXPOSE 443

# 7 - Download weights
RUN wget -c -N http://joachimveulemans.be/vehicle.weights -P models/
RUN wget -c -N http://joachimveulemans.be/lp.weights -P models/

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
