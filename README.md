# mini-launchpad

Debian package building and delivery in a box. The purpose of this project is
to provide the services to accept Debian source packages and build Debian
binary packages with minimal setup and configuration. The goal is to setup the
build system without a website GUI frontend. Initially, we are targeting Ubuntu
package builds.

# Setup Instructions

Build the mini-dinstall and mini-launchpad images:

    $ cd docker
    $ docker-compose -p mlp build mini-launchpad mini-dinstall
    
Setup the pbuilder environments inside of the mini-launchpad container / volume
(This can take a long time and it will be running in "privileged" mode):
    
    $ docker-compose -p mlp run mini-launchpad
    
If the previous docker-compose command exited without error, we can now startup
the entire mini-launchpad system:

    $ docker-compose -p mlp up -d mini-launchpad mini-dinstall mini-dinstall-web

The user has to edit the docker.compose.yml file to set the PUBLICHOST to their
IP address. It defaults to 127.0.0.1

Stop docker processes:

    $ docker-compose -p mlp stop

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
