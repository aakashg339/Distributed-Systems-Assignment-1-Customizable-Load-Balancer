# Using Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Setting the working directory to '/server'
WORKDIR /dockerLoadBalancer

# Copying current directory content to '/server'
COPY . /dockerLoadBalancer

# Installing dependencies
RUN apt-get update
RUN apt-get -y install sudo
# Setting timezone which is required for docker installation
RUN apt-get update && \
    apt-get -y install sudo tzdata && \
    sudo ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    sudo dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get clean

RUN for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
RUN sudo apt-get update
RUN sudo apt-get install -y ca-certificates curl gnupg
RUN sudo install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN sudo apt-get update
# Installing docker related components
RUN sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Installing python3, pip3 and other dependencies(flask)
RUN apt-get install -y python3 python3-pip && pip3 install flask && pip3 install requests

ENV USER=theuser
RUN adduser --home /home/$USER --disabled-password --gecos GECOS $USER \
  && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
  && chmod 0440 /etc/sudoers.d/$USER \
  && usermod -aG docker $USER \
  && chsh -s /bin/zsh $USER
USER $USER

ENV HOME=/home/$USER

# Exposing port 5000
EXPOSE 5000

# Running the server
ENTRYPOINT python3 load_balancer.py