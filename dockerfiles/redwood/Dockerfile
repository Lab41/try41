from ubuntu:raring
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-04-14
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN sed 's/us-east-1.ec2.archive.ubuntu.com/nova.clouds.archive.ubuntu.com/' -i /etc/apt/sources.list
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update

RUN apt-get install -y build-essential
RUN apt-get install -y pwgen
RUN apt-get install -y g++-4.7 c++-4.7
RUN apt-get install -y npm
RUN apt-get install -y python-setuptools
RUN easy_install pip
RUN apt-get install -y python-matplotlib
RUN apt-get install -y python-mysqldb
RUN apt-get install -y python-numpy
RUN apt-get install -y python-scipy
RUN apt-get install -y git
RUN npm config set registry http://registry.npmjs.org/
RUN npm install tty.js

# sets root password to root, but isn't accessible from the outside
RUN echo 'mysql-server-5.5 mysql-server/root_password password password' | debconf-set-selections
RUN echo 'mysql-server-5.5 mysql-server/root_password_again password password' | debconf-set-selections

RUN apt-get update && apt-get install -y mysql-server && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

ENV REDWOOD_PULLED_AT 2014-04-14
RUN git clone https://github.com/Lab41/Redwood.git
ADD visual.py /Redwood/redwood/helpers/visual.py
ADD redwood /Redwood/bin/redwood
RUN rm -rf /Redwood/Filters/file_types.py
RUN mkdir /Redwood/reports/output
RUN mkdir /Redwood/reports/output/reports
RUN mv /Redwood/reports/resources /Redwood/reports/output/reports/resources
RUN cd /Redwood; python setup.py install

ADD . /src

EXPOSE 8000 8080

CMD ["/bin/bash", "/src/startup.sh"]
