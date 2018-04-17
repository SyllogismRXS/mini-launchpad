FROM ubuntu:16.04

MAINTAINER Kevin DeMarco

RUN apt-get update && apt-get install -y pbuilder ubuntu-dev-tools \
    debootstrap ubuntu-keyring debian-archive-keyring wget

RUN wget -qO - http://repos.rcn-ee.net/ubuntu/conf/repos.rcn-ee.net.gpg.key | \
    apt-key add -

ADD pbuilderrc /root/.pbuilderrc

RUN dpkg --add-architecture armhf && \
    dpkg --add-architecture arm64 && \
    dpkg --add-architecture i386

RUN apt-get install -y build-essential crossbuild-essential-armhf \
    crossbuild-essential-arm64 qemu-user-static

RUN echo 'USENETWORK=yes' | sudo tee -a /etc/pbuilderrc

ADD start.sh /root/start.sh

CMD ["/root/start.sh"]
