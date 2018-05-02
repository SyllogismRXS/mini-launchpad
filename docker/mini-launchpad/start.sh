#!/bin/bash

dist="xenial"

#declare -a arch_array=("amd64" "arm64" "armhf" "i386")
declare -a arch_array=("amd64")

#for arch in "${arch_array[@]}"
#do
#   arch_str="${arch_str} ${arch}"

#   if [ ! -f /var/cache/pbuilder/${dist}-${arch}-base.tgz ]; then
#       DIST=${dist} ARCH=${arch} pbuilder --create \
#           --configfile /home/gtri-uav/.pbuilderrc
#   else
#       DIST=${dist} ARCH=${arch} pbuilder --update \
#           --configfile /home/gtri-uav/.pbuilderrc
#   fi
#done

echo "============================================="
echo "pbuilder environment configuration complete"
echo "============================================="

python -u /home/gtri-uav/mini-launchpad/mini-launchpad/mini-launchpad --dist xenial \
                                  --arch ${arch_str} \
                                  --ftp-incoming /home/gtri-uav/test \
				  --ftp-incoming-clear true \
                                  --pbuilder-config /home/gtri-uav/.pbuilderrc \
                                  --dput-config /home/gtri-uav/.dput.cf \
                                  --dput-name local \
                                  --log-path /home/gtri-uav/build-logs
