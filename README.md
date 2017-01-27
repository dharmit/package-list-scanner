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

- List rpm packages in CentOS based image:

    ```
    $ atomic scan --scanner package-list-scanner --rootfs=/mnt registry.centos.org/centos/centos
    ```

  At the moment, it's kinda hard-coded to use `/mnt` for mounting container's
rootfs. If you opt to use a different directory instead, you might need to make
changes to `rpm-list.sh` script.

- List pip packages in CentOS based image:

    ```
    $ IMAGE_NAME=<image-name> atomic scan --scanner pacakge-list-scanner --scan_type pip-list <image-name>
    ```

  Similarly for list of packages installed via npm (global packages) and gem,
replace `pip-list` in `--scan_type` for above command with `npm-list` and
`gem-list` respectively.

