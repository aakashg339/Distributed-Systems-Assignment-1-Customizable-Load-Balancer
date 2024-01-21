# Using Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Setting the working directory to '/server'
WORKDIR /dockerServer

# Copying current directory content to '/server'
COPY . /dockerServer

# Installing python3, pip3 and other dependencies(flask)
RUN apt-get update
RUN apt-get -y install sudo

RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get -y install docker-ce-cli

ENV USER=theuser
RUN adduser --home /home/$USER --disabled-password --gecos GECOS $USER \
  && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
  && chmod 0440 /etc/sudoers.d/$USER \
  && groupadd docker \
  && usermod -aG docker $USER \
  && chsh -s /bin/zsh $USER
USER $USER

ENV HOME=/home/$USER

# Exposing port 5000
EXPOSE 5000

# Running the server
ENTRYPOINT python3 load_balancer.py