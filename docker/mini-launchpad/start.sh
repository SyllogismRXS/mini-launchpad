#!/bin/bash

dist="xenial"

declare -a arch_array=("amd64" "arm64" "armhf" "i386")

for arch in "${arch_array[@]}"
do
    if [ ! -f /var/cache/pbuilder/${dist}-${arch}-base.tgz ]; then
        DIST=${dist} ARCH=${arch} pbuilder --create
    else
        DIST=${dist} ARCH=${arch} pbuilder --update
    fi
done
