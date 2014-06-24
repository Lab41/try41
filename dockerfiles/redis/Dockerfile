FROM ubuntu:trusty
MAINTAINER Charlie Lewis <charliel@lab41.org>

RUN apt-get update
RUN apt-get install -y redis-server

RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

RUN addgroup docker
RUN adduser --ingroup docker --disabled-login --system docker
RUN touch /etc/rsyslog.d/50-default.conf
RUN chown docker:docker /etc/rsyslog.d/50-default.conf
RUN echo "docker ALL=NOPASSWD: /etc/init.d/rsyslog start" >> /etc/sudoers

WORKDIR /home/docker
USER docker

EXPOSE 6379

CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; \
    sudo /etc/init.d/rsyslog start; \
    logger started redis container $PARENT_HOST; \
    /usr/bin/redis-server
