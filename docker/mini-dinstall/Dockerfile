FROM ubuntu:16.04

MAINTAINER Kevin DeMarco

RUN apt-get update && \
    apt-get install -y git python dput procps less python-apt apt-utils

RUN git clone https://github.com/shartge/mini-dinstall.git
WORKDIR mini-dinstall
RUN git checkout e50008e081cc87fd0e7de1b8d72d1f91389a5601

# os.rename throws exceptions when renaming files that are in shared volumes,
# so we need to change these calls to shutil.move calls
RUN sed -i -- "s/os.rename/shutil.move/g" ./mini-dinstall

RUN python setup.py install

COPY mini-dinstall.conf /root/.mini-dinstall.conf

RUN mkdir -p /root/archive

COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
CMD /root/start.sh
