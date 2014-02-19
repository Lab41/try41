from boxcar/raring
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-02-18
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN sed 's/us-east-1.ec2.archive.ubuntu.com/nova.clouds.archive.ubuntu.com/' -i /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

# Keep upstart from complaining
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN apt-get install -y pwgen
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install -y g++-4.7 c++-4.7
RUN apt-get install -y xorg openbox
RUN apt-get install -y node
RUN apt-get install -y npm
RUN npm config set registry http://registry.npmjs.org/
RUN npm install tty.js

ADD . /src

EXPOSE 8000 8080

CMD ["/bin/bash", "/src/startup.sh"]
