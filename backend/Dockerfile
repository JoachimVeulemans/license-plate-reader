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

# 6 - Copy whole project to Docker container
COPY . /app

# 7 - Set environment to use port 443
ENV PORT 443

# 8 - Expose port 443 to bind to later on
EXPOSE 443

# 9 - Define the working directory
WORKDIR /app

# 10 - Set entrypoint to Python
ENTRYPOINT [ "python3.6" ]

# 11 - Launch app.py in command line
CMD [ "app.py" ]