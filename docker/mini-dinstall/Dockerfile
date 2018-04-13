FROM stilliard/pure-ftpd

MAINTAINER Kevin DeMarco

RUN apt-get update && \
    apt-get install -y dput mini-dinstall rsync procps less

# Setup mini-dinstall
COPY mini-dinstall.conf /root/.mini-dinstall.conf

# Run mini-dinstall (runs as daemon)
RUN mini-dinstall --config=/root/.mini-dinstall.conf

# Setup ftp anonymous user
RUN useradd -m ftp
ENV FTP_ANON_DIR /home/ftp

# Create symbolic link from ftp server to incoming directory
RUN rm -r /root/archive/mini-dinstall/incoming && \
    ln -s /home/ftp /root/archive/mini-dinstall/incoming

# Setup htdocs directory
RUN mkdir -p /root/htdocs

# Setup the cronjob
RUN apt-get -y install cron
# Add crontab file in the cron directory
ADD copy-archive-cron copy-archive-cron
# Give execution rights on the cron job
RUN crontab copy-archive-cron

# Setup start.sh script that concurrently runs mini-dinstall and pure-ftpd
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
CMD /root/start.sh
