#!/bin/bash

dist="xenial"

declare -a arch_array=("amd64" "arm64" "armhf" "i386")

for arch in "${arch_array[@]}"
do
    if [ ! -f /var/cache/pbuilder/${dist}-${arch}-base.tgz ]; then
        DIST=${dist} ARCH=${arch} pbuilder --create \
            --configfile=/root/.pbuilderrc
    else
        DIST=${dist} ARCH=${arch} pbuilder --update \
            --configfile=/root/.pbuilderrc
    fi
done

echo "============================================="
echo "pbuilder environment configuration complete"
echo "============================================="

/usr/bin/mini-launchpad --dist xenial \
                        --arch amd64 armhf i386 arm64 \
                        --ftp-loc /root/incoming \
                        --pbuilder-config /root/.pbuilderrc \
                        --dput-config /root/.dput.cf \
                        --dput-name local-ftp \
