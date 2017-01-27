FROM registry.centos.org/centos/centos
MAINTAINER Dharmit Shah <dharmit@redhat.com>

LABEL INSTALL='docker run -it --rm --privileged -v /etc/atomic.d:/host/etc/atomic.d/ $IMAGE sh /install.sh'

RUN yum -y update && \
    yum -y install python-docker-py && \
    yum clean all

ADD package-list-scanner rpm-list.sh scanner.py install.sh /
