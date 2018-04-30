FROM stilliard/pure-ftpd

MAINTAINER Kevin DeMarco

# Setup ftp anonymous user
RUN useradd -m ftp
ENV FTP_ANON_DIR /home/ftp

CMD /run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -j -S $LISTEN_PORT -P $PUBLICHOST -p $PORT_RANGE
