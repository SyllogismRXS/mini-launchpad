#!/bin/bash

declare -a dist_array=("xenial" "bionic")
declare -a arch_array=("amd64" "arm64" "armhf" "i386")

for dist in "${dist_array[@]}"
do
    for arch in "${arch_array[@]}"
    do
	if [ ! -f /var/cache/pbuilder/${dist}-${arch}-base.tgz ]; then
            DIST=${dist} ARCH=${arch} pbuilder --create \
		--configfile /root/.pbuilderrc
	else
            DIST=${dist} ARCH=${arch} pbuilder --update \
		--configfile /root/.pbuilderrc --override-config
	fi
    done
done

# Build the dist_str
for dist in "${dist_array[@]}"
do
    dist_str="${dist_str} ${dist}"
done

# Build the arch_str
for arch in "${arch_array[@]}"
do
    arch_str="${arch_str} ${arch}"
done

echo "============================================="
echo "pbuilder environment configuration complete"
echo "============================================="

python -u /usr/bin/mini-launchpad --dist ${dist_str} \
                                  --arch ${arch_str} \
                                  --ftp-incoming /root/incoming \
                                  --pbuilder-config /root/.pbuilderrc \
                                  --dput-config /root/.dput.cf \
                                  --dput-name local-sftp \
                                  --log-path /root/build-logs
