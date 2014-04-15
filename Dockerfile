from ubuntu:saucy
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-04-14
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y git
RUN apt-get install -y python-setuptools
RUN easy_install pip
ADD api.py /try-challenges/api.py
ADD requirements.txt /try-challenges/requirements.txt
ADD patch /try-challenges/patch
ADD static /try-challenges/static
ADD templates /try-challenges/templates
RUN pip install -r /try-challenges/requirements.txt
ADD patch/auth.py /usr/local/lib/python2.7/dist-packages/docker/auth/auth.py
ADD patch/client.py /usr/local/lib/python2.7/dist-packages/docker/client.py

EXPOSE 5000

WORKDIR /try-challenges
CMD sed -i "s/127.0.0.1/$SUBDOMAIN/g" /try-challenges/api.py; python api.py
