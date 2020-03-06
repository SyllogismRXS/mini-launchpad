FROM ubuntu:18.04

MAINTAINER Kevin DeMarco
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y pbuilder ubuntu-dev-tools \
    debootstrap ubuntu-keyring debian-archive-keyring wget build-essential \
    crossbuild-essential-armhf crossbuild-essential-arm64 qemu \
    cmake python systemd python-pip python3-paramiko zlib1g-dev \
    pkg-config libglib2.0-dev binutils-dev libboost-all-dev \
    autoconf libtool libssl-dev libpixman-1-dev libpython-dev \
    python-capstone virtualenv binutils-dev

# Install python packages required by mini-launchpad
RUN pip install watchdog argparse

RUN apt-get install -y qemu-user-static

# Build newer version of qemu
RUN wget https://download.qemu.org/qemu-4.2.0.tar.xz \
    && tar xvJf qemu-4.2.0.tar.xz \
    && cd qemu-4.2.0 \
    && ./configure --prefix=$(cd ..; pwd)/qemu-user-static \
                   --static \
		   --disable-system \
		   --enable-linux-user \
    && make -j7 \
    && make install \
    && cd ../qemu-user-static/bin \
    && for i in *; do cp $i $i-static; done \
    && cp * /usr/bin/

# Setup cross-build environment
RUN wget -qO - http://repos.rcn-ee.net/ubuntu/conf/repos.rcn-ee.net.gpg.key | \
    apt-key add -

RUN dpkg --add-architecture armhf && \
    dpkg --add-architecture arm64 && \
    dpkg --add-architecture i386

RUN echo 'USENETWORK=yes' | sudo tee -a /etc/pbuilderrc

# Copy over mini-launchpad cmake project and code
RUN mkdir -p /root/mini-launchpad
COPY . /root/mini-launchpad/

# Move .pbuilderrc and .dput.cf to their standard locations
RUN mv /root/mini-launchpad/docker/mini-launchpad/pbuilderrc /root/.pbuilderrc && \
    mv /root/mini-launchpad/docker/mini-launchpad/dput.cf /root/.dput.cf

# Install the service
WORKDIR /root/mini-launchpad
RUN mkdir -p ./build
WORKDIR build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=/usr && make install

CMD ["/root/mini-launchpad/docker/mini-launchpad/start.sh"]
