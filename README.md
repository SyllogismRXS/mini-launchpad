# mini-launchpad

Debian package building and delivery in a box. The purpose of this project is
to provide the services to accept Debian source packages and build Debian
binary packages with minimal setup and configuration. The goal is to setup the
build system without a website GUI frontend. Initially, we are targeting Ubuntu
package builds.

# Setup Instructions

Emulator is required to be installed in host machine for the arm builds to work:

    $ apt-get install qemu-user-static

Build the mini-dinstall and mini-launchpad images:

    $ cd docker
    $ docker-compose -p mlp build pure-ftpd-1 mini-launchpad mini-dinstall

Setup the pbuilder environments inside of the mini-launchpad container / volume
(This can take a long time and it will be running in "privileged" mode):

    $ docker-compose -p mlp up mini-launchpad

After "pbuilder environment configuration complete" is printed to the terminal,
type ``CTRL+c`` to stop the mini-launchpad docker container. We can now startup
the entire mini-launchpad system:

    $ docker-compose -p mlp up -d mini-launchpad mini-dinstall-web

# Setup Repository Sources

Add the following line to your ``/etc/apt/sources.list`` file:

    deb [trusted=yes] http://localhost/archive xenial/<ARCH>/

where, ``<ARCH>`` could be amd64, armhf, i386, arm64, etc. Now update your
sources and check the policy for a package you pushed to your server:

    $ sudo apt-get update
    $ apt-cache policy <package-name>

# Shutdown mini-launchpad

    $ docker-compose -p mlp stop

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
