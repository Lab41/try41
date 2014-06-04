FROM ubuntu:trusty
MAINTAINER Charlie Lewis <charliel@lab41.org>

RUN apt-get update
RUN apt-get install -y redis-server

RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

EXPOSE 6379

CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; /etc/init.d/rsyslog start; logger started redis container; /usr/bin/redis-server
