FROM ubuntu:16.04

MAINTAINER Kevin DeMarco

# RUN apt-get update && apt-get install -y pbuilder ubuntu-dev-tools \
#     debootstrap ubuntu-keyring debian-archive-keyring wget build-essential \
#     crossbuild-essential-armhf crossbuild-essential-arm64 qemu-user-static
#
# RUN wget -qO - http://repos.rcn-ee.net/ubuntu/conf/repos.rcn-ee.net.gpg.key | \
#     apt-key add -
#
# RUN dpkg --add-architecture armhf && \
#     dpkg --add-architecture arm64 && \
#     dpkg --add-architecture i386
#
# RUN echo 'USENETWORK=yes' | sudo tee -a /etc/pbuilderrc

RUN apt-get update && apt-get install -y cmake python systemd

RUN apt-get install -y build-essential

# Install python packages required by mini-launchpad
RUN apt-get install -y python-pip
RUN pip install watchdog argparse

# Copy over mini-launchpad cmake project and code
RUN mkdir -p /root/mini-launchpad
COPY . /root/mini-launchpad/

# Install the service
WORKDIR /root/mini-launchpad
RUN mkdir ./build
WORKDIR build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=/usr && make install

CMD ["/root/mini-launchpad/docker/mini-launchpad/start.sh"]
