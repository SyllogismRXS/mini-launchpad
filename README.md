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

Create a `.env` file for docker-compose that contains the server's
public IP address. If you want to be able to use `dput` from a remote
machine (due to the ftp server's passive mode), you must substitute
the server's IP address for `localhost` in the following command:

    $ echo "PUBLICHOST=localhost" > ./docker/.env

Likewise, change `localhost` to the server's IP address in
`./docker/mini-launchpad/dput.cf`.

Build the docker images:

    $ cd docker
    $ docker-compose -p mlp build

Setup the pbuilder environments inside of the mini-launchpad container /
volume.  The following can take a long time (~30 minutes) and it will be
running in "privileged" mode:

    $ docker-compose -p mlp up mini-launchpad

After `pbuilder environment configuration complete` is printed to the
terminal, type `CTRL+c` to stop the mini-launchpad docker container. We can
now startup the entire mini-launchpad system:

    $ docker-compose -p mlp up -d

Everytime mini-launchpad starts up, it refreshes the available debian
packages using the apt-get sources defined in
`./docker/mini-launchpad/pbuilderrc` for each of the pbuilder
environments. This can take about five minutes and needs to be
completed before packages can be uploaded.

You can view the terminal output from the mini-launchpad system with
the `docker-compose` `logs` command:

    $ docker-compose -p mlp logs -f

## Shutdown mini-launchpad

    $ docker-compose -p mlp stop

# Local Machine Setup Instructions

The following are the setup instructions on your local machine, not the
server. On a local machine, you may use dput to push debian source packages to
mini-launchpad or use dput to push debian binary packages (that you have built
locally) to reprepro.

## Setup local ~/.dput.cf configuration

In order to upload debian source and binary packages to mini-launchpad, you
need to configure your `~/.dput.cf` file (See
[dput documentation](http://manpages.ubuntu.com/manpages/xenial/man1/dput.1.html)).
An example `dput.cf` file is provided with this repository. Update your own
`~/.dput.cf` file to include the information from `dput.cf`. Once updated, you
can upload a debian source package with the following command:

    $ dput server-source /path/to/<package>_source.changes

If you want to build a local version of a debian package and upload it directly
to reprepro (bypassing the mini-launchpad build process), use the following
dput command:

    $ dput server-binary /path/to/<package>_<arch>.changes

## Setup Repository Sources

In order to download and install (using apt-get) the debian packages built by
mini-launchpad, you need to configure the sources.list file on your local
machine.

Add the following line to your `/etc/apt/sources.list` file:

    deb [trusted=yes] http://<SERVER-IP>/archive/ xenial main

where `<SERVER-IP>` is the server's IP address. Now update your
sources and check the policy for a package you pushed to your server:

    $ sudo apt-get update
    $ apt-cache policy <package-name>

## Removing packages from server

See the [reprepro
documentation](https://manpages.debian.org/stretch/reprepro/reprepro.1.en.html)

To remove packages from the server, login to the reprepro container:

    $ docker exec -it mlp_reprepro_1 /bin/bash

You can use `reprepro` to manage the debian packages. For example, to
list the available xenial packages run the following command:

    $ reprepro -b /var/repositories list xenial

To remove a package, run the following command:

    $ reprepro -b /var/repositories remove xenial <package-name>

## Access Build Logs

Open a browser and navigate to `http://<SERVER-IP>:9080/build-logs`

# Other Related Projects

[mini-buildd](http://mini-buildd.installiert.net/)

[Open Build Service](http://openbuildservice.org/)
