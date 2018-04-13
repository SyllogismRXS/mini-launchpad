#!/bin/bash

service cron start

mini-dinstall --config=/root/.mini-dinstall.conf

/run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -j -P $PUBLICHOST -p 30000:30009
