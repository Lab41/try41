from ubuntu:precise
MAINTAINER Charlie Lewis <charliel@lab41.org>

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update --fix-missing; \
    apt-get install -y python-software-properties; \
    apt-add-repository ppa:chris-lea/node.js; \
    apt-get update; \
    apt-get install -y -q wget \
                          curl \
                          git \
                          maven \
                          bzip2 \
                          supervisor \
                          nodejs \
                          dpkg \
                          tomcat7 \
                          gnuplot \
                          openssh-server \
                          gcc \
                          g++ \
                          build-essential \
                          libopenmpi-dev \
                          openmpi-bin \
                          default-jdk \
                          cmake \
                          zlib1g-dev \
                          make
