FROM ubuntu:18.04

MAINTAINER Kevin DeMarco

ENV DEBIAN_FRONTEND noninteractive
SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y \
               reprepro \
               python \
               python-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install \
    argparse \
    watchdog

# Setup reprepro directory structure
RUN mkdir -p /var/repositories \
    mkdir -p /root/incoming

# Copy in the python program that will watch the incoming directory
ADD incoming.py /root/incoming.py

CMD /root/incoming.py --base-repository /var/repositories \
                      --distribution ${DISTRIBUTION} \
                      --incoming-dir /root/incoming
