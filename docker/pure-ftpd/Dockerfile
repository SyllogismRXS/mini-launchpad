FROM stilliard/pure-ftpd

MAINTAINER Kevin DeMarco

# Setup ftp anonymous user
RUN useradd -m ftp
ENV FTP_ANON_DIR /home/ftp

CMD /run.sh -c 5 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -j -P $PUBLICHOST -p $PORT_RANGE
