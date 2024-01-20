# Using Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Setting the working directory to '/server'
WORKDIR /dockerServer

# Copying current directory content to '/server'
COPY . /dockerServer

# Installing python3, pip3 and other dependencies(flask)
RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install flask

# Exposing port 5000
EXPOSE 5000

# Running the server
ENTRYPOINT python3 server.py