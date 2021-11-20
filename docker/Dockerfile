# Get Base image
FROM ubuntu:latest

# Maintain Label
ARG IMAGE_NAME='sarvesh030195/python-automation:v1'

# Set working directory
USER root
WORKDIR /root

# Essential Setup
RUN apt-get --assume-yes --allow-unauthenticated clean && \
    apt-get --assume-yes --allow-unauthenticated update && \
    apt-get --assume-yes --allow-unauthenticated install build-essential vim wget libssl-dev python-dev python3-dev \
    python3-pip python3.9-dev python3.9-venv

RUN apt-get --assume-yes --allow-unauthenticated install git python3.9 && \
    ln -fs /usr/bin/python3.9 /usr/bin/python3

# Python Packages
RUN python3 -m pip install --no-cache-dir --quiet --upgrade setuptools pyopenssl shyaml pip bc yq wheel virtualenv