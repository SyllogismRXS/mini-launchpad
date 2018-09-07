# mini-launchpad

Debian package building and delivery in a box. The purpose of this project is
to provide the services to accept Debian source packages and build Debian
binary packages with minimal setup and configuration. The goal is to setup the
build system without a website GUI frontend. Initially, we are targeting Ubuntu
package builds.

# Server Setup Instructions

The following are the setup instructions to be run on the machine that will
host the mini-launchpad server.

An emulator is required to be installed in host machine for the arm builds to
work:

    $ apt-get install qemu-user-static

Modify the ``./docker/docker-compose.yml`` file by changing ``PUBLICHOST:
"localhost"`` to use your specific server IP address for passive FTP uploads
for both pure-ftpd services. Also, modify the ``fqdn`` line in
``./docker/mini-launchpad/dput.cf`` to point to your server's IP address (e.g.,
``fqdn = 192.168.1.139:8021``). Just using ``localhost`` breaks the PASV FTP
functionality.

Build the docker images:

    $ cd docker
    $ docker-compose -p mlp build

Setup the pbuilder environments inside of the mini-launchpad container /
volume.  The following can take a long time (~20 minutes) and it will be
running in "privileged" mode:

    $ docker-compose -p mlp up mini-launchpad

After ``pbuilder environment configuration complete`` is printed to the
terminal, type ``CTRL+c`` to stop the mini-launchpad docker container. We can
now startup the entire mini-launchpad system:

    $ docker-compose -p mlp up -d

## Shutdown mini-launchpad

    $ docker-compose -p mlp stop

# Local Machine Setup Instructions

The following are the setup instructions on your local machine, not the
server. On a local machine, you may use dput to push debian source packages to
mini-launchpad or use dput to push debian binary packages (that you have built
locally) to mini-dinstall.

## Setup local ~/.dput.cf configuration

In order to upload debian source and binary packages to mini-launchpad, you
need to configure your ``~/.dput.cf`` file.  An example ``dput.cf`` file is
provided with this repository. Update your own ``~/.dput.cf`` file to include
the information from ``dput.cf``. Once updated, you can upload a debian source
package with the following command:

    $ dput server-source /path/to/<package>_source.changes

If you want to build a local version of a debian package and upload it directly
to mini-dinstall (bypassing the mini-launchpad build process), use the
following dput command:

    $ dput server-binary /path/to/<package>_<arch>.changes

## Setup Repository Sources

In order to download and install (using apt-get) the debian packages built by
mini-launchpad, you need to configure the sources.list file on your local
machine.

Add the following line to your ``/etc/apt/sources.list`` file:

    deb [trusted=yes] http://<SERVER-IP>/archive xenial/<ARCH>/

where, ``<ARCH>`` could be amd64, armhf, i386, arm64, etc and ``<SERVER-IP>``
is the server's IP address. Now update your sources and check the policy for a
package you pushed to your server:

    $ sudo apt-get update
    $ apt-cache policy <package-name>

## Removing packages in mini-dinstall

To remove packages from the server, login to the mini-dinstall container:

    $ docker exec -it mlp_mini-dinstall_1 /bin/bash

From there you will want to navigate to the directory where the packages live:

    $ cd ~/archive/xenial

Here we should have all our packages organized by supported architectures. The
next step is to remove all instances of the package we want to remove. (To
double check what files you'll be purging remove the -delete flag).

    $ find . -name "dumby-package*" -type f -delete

Lastly, we want to remove the *.db files located in this directory as they keep
stored information about packages uploaded and don't update when the same
package is sent to the server causing conflicts when attempting to fetch it
later on.

    $ rm *.db

## Hash Sum mismatch Error

If you receive a "Hash Sum mismatch" error when trying to install packages with
apt-get, the "Packages" file on the server may have to be regenerated. This is
mostly easily accomplished by removing the ``*.db`` files on the server and
restarting mini-launchpad. For example,

    $ docker exec -it mlp_mini-dinstall_1 /bin/bash
    $ cd ~/archive/xenial.db
    $ rm *.db
    $ exit                            # exit the mini-dinstall container
    $ docker-compose -p mlp stop      # stop mini-launchpad
    $ docker-compose -p mlp up -d     # start mini-launchpad
    $ docker-compose -p mlp logs -f   # Check mini-dinstall logs

The client computer's (where apt-get install is run) cached version of the
Packages file has to be removed as well:

    $ sudo rm -rf /var/lib/apt/lists/*
    $ sudo apt-get update

## Access Build Logs

Open a browser and navigate to ``http://<SERVER-IP>:9080/build-logs``

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
