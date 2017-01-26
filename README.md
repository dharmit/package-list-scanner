Atomic scanner: rpm-list-scanner
--------------------------------

This is a container image scanner based on `atomic scan`. The goal of the
scanner is to list the packages installed in a container image.

Steps to use:

- Pull container image:

    ```
    $ docker pull registry.centos.org/dharmit/package-list-scanner
    ```

- Install it using `atomic`:

    ```
    $ atomic install registry.centos.org/dharmit/package-list-scanner
    ```

- Mount the image's rootfs because by default `atomic scan` would mount it in
  read-only mode but we need read-write capability:

    ```
    $ atomic mount -o rw registry.centos.org/centos/centos /mnt
    ```

Make sure you have `centos:centos7` available locally before you try to mount

- Run the scanner on CentOS based images:

    ```
    $ atomic scan --scanner rpm-list-scanner --rootfs=/mnt registry.centos.org/centos/centos
    ```

###NOTE

1. At the moment, it's kinda hard-coded to use `/mnt` for mounting container's
rootfs. If you opt to use a different directory instead, you might need to make
changes to `rpm-list.sh` script. I haven't tested it yet.

2. Once you do `atomic install` you'll see a scan type called `pip-list` under
   `atomic scan --list` for the scanner `package-list-scanner`. This scan type
hasn't been implemented yet but will be done shortly.
