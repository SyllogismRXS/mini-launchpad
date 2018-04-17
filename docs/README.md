Docs
====

Description
-----------

In the spirit of docker's "separation of services," the mini-launchpad system
runs in four different docker containers. One exception is docker container 3,
where pure-ftpd and mini-dinstall run in the same container. This is due to a
bug in how mini-dinstall moves files (it fails to move files that are in shared
volumes). To work around this, the pure-ftpd server and mini-dinstall share a
standard symbolic link within the same container. The output of mini-dinstall
is an apt-get repository that can be hosted on a web server. The output of
mini-dinstall is rsync'd to a shared volume with httpd (again to work around
the mini-dinstall bug). (TODO: Investigate fixing mini-dinstall's move-files
bug).

mini-launchpad has to run inside of a "privileged" docker container because it
uses chroot to build packages. (TODO: investigate use of reduced
[privileges](https://blog.docker.com/2017/10/least-privilege-container-orchestration/)).


Other Notes
-----------
Use [yEd](https://www.yworks.com/products/yed) to edit graphml files.

