from boxcar/raring
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-02-25
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN sed 's/us-east-1.ec2.archive.ubuntu.com/nova.clouds.archive.ubuntu.com/' -i /etc/apt/sources.list
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get upgrade -y

# Keep upstart from complaining
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN apt-get install -y pwgen
RUN apt-get install -y g++-4.7 c++-4.7
RUN apt-get install -y node
RUN apt-get install -y npm
RUN apt-get install -y python-setuptools
RUN easy_install pip
RUN pip install texttable
RUN pip install requests
RUN apt-get install -y python-mysqldb
RUN apt-get install -y git
RUN npm config set registry http://registry.npmjs.org/
RUN npm install tty.js

# sets root password to password, but isn't accessible from the outside
RUN echo 'mysql-server-5.5 mysql-server/root_password password password' | debconf-set-selections
RUN echo 'mysql-server-5.5 mysql-server/root_password_again password password' | debconf-set-selections

RUN apt-get update && apt-get install -y mysql-server && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

ENV REDWOOD_PULLED_AT 2014-02-25
RUN git clone https://github.com/Lab41/Hemlock.git
RUN cd /Hemlock; python setup.py install

ADD . /src

EXPOSE 8000 8080

CMD ["/bin/bash", "/src/startup.sh"]
