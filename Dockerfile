from ubuntu:trusty
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-04-14
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y git
RUN apt-get install -y python-setuptools
RUN easy_install pip
ADD api.py /try41/api.py
ADD requirements.txt /try41/requirements.txt
ADD patch /try41/patch
ADD static /try41/static
ADD templates /try41/templates
RUN pip install -r /try41/requirements.txt
ADD patch/auth.py /usr/local/lib/python2.7/dist-packages/docker/auth/auth.py
ADD patch/client.py /usr/local/lib/python2.7/dist-packages/docker/client.py

# add rsyslog
RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

EXPOSE 5000

WORKDIR /try41
CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; /etc/init.d/rsyslog start; logger started try41 container; sed -i "s/127.0.0.1/$SUBDOMAIN/g" /try41/api.py; sed -i "s/localhost/$REDIS_HOST/g"; python api.py
