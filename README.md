# mini-launchpad

Debian package building and delivery in a box. The purpose of this project is
to provide the services to accept Debian source packages and build Debian
binary packages with minimal setup and configuration. The goal is to setup the
build system without a website GUI frontend. Initially, we are targeting Ubuntu
package builds.

# Setup Instructions

Emulator is required to be installed in host machine for the arm builds to
work:

    $ apt-get install qemu-user-static

Build the mini-dinstall and mini-launchpad images:

    $ cd docker
    $ docker-compose -p mlp build pure-ftpd-1 mini-launchpad pure-ftpd-2 \
        mini-dinstall mini-dinstall-web mini-launchpad-web

Modify the docker-compose.yml file to change ``PUBLICHOST: "localhost"`` to use
your specific server IP address for passive FTP uploads for both pure-ftpd
services.

Setup the pbuilder environments inside of the mini-launchpad container / volume
(This can take a long time and it will be running in "privileged" mode):

    $ docker-compose -p mlp up mini-launchpad

After "pbuilder environment configuration complete" is printed to the terminal,
type ``CTRL+c`` to stop the mini-launchpad docker container. We can now startup
the entire mini-launchpad system:

    $ docker-compose -p mlp up -d pure-ftpd-1 mini-launchpad pure-ftpd-2 \
        mini-dinstall mini-dinstall-web mini-launchpad-web

# Setup Repository Sources

Add the following line to your ``/etc/apt/sources.list`` file:

    deb [trusted=yes] http://<SERVER-IP>/archive xenial/<ARCH>/

where, ``<ARCH>`` could be amd64, armhf, i386, arm64, etc and ``<SERVER-IP>``
is the server's IP address. Now update your sources and check the policy for a
package you pushed to your server:

    $ sudo apt-get update
    $ apt-cache policy <package-name>

# Access Build Logs

Open a browser and navigate to ``http://<SERVER-IP>:9080/build-logs``

# Shutdown mini-launchpad

    $ docker-compose -p mlp stop

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
