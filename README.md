# mini-launchpad

Debian package building and delivery in a box. The purpose of this project is
to provide the services to accept Debian source packages and build Debian
binary packages with minimal setup and configuration. The goal is to setup the
build system without a website GUI frontend. Initially, we are targeting Ubuntu
package builds.

# Setup Instructions

TODO: Eventually, I want a user to be able to git clone this repo and just be
able to run a docker-compose command to start up mini-launchpad.

The user has to edit the docker.compose.yml file to set the PUBLICHOST to their
IP address. It defaults to 127.0.0.1

Build docker images and run:

    $ cd docker
    $ docker-compose -p mlp build mini-dinstall
    $ docker-compose -p mlp up -d mini-dinstall mini-dinstall-web
    
Stop docker processes:

    $ docker-compose -p mlp stop

TODO: We need to figure out if we can run pbuilder inside of docker in a safe
way. For now, only mini-dinstall, its pure-ftpd server, and the apache2 server
that delivers the package binaries are in docker.

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
