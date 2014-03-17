from boxcar/raring
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-02-27
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN sed 's/us-east-1.ec2.archive.ubuntu.com/nova.clouds.archive.ubuntu.com/' -i /etc/apt/sources.list
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get update

# Keep upstart from complaining
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN apt-get install -y python2.7
RUN apt-get install -y pwgen
RUN apt-get install -y g++-4.7 c++-4.7
RUN apt-get install -y node
RUN apt-get install -y npm
RUN apt-get install -y python-setuptools
RUN easy_install pip
RUN pip install texttable
RUN pip install requests
RUN pip install six==1.5.2
RUN pip install pyes
RUN apt-get install -y python-mysqldb
RUN apt-get install -y git
RUN npm config set registry http://registry.npmjs.org/
RUN npm install tty.js

# elasticsearch
RUN apt-get install -y openjdk-6-jdk
RUN apt-get install -y wget
RUN apt-get install -y dpkg
RUN apt-get install -y unzip
RUN wget --no-check-certificate https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.2.deb
RUN dpkg -i elasticsearch-0.90.2.deb
RUN /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head

# couchbase
ENV CB_VERSION 2.0.1
ENV CB_DOWNLOAD_URL http://packages.couchbase.com/releases
ENV CB_PACKAGE couchbase-server-community_x86_64_$CB_VERSION.deb
ENV CB_USERNAME         Administrator
ENV CB_PASSWORD         password

# Limits
RUN sed -i.bak '/\# End of file/ i\\# Following 4 lines added by docker-couchbase-server' /etc/security/limits.conf
RUN sed -i.bak '/\# End of file/ i\\*                hard    memlock          unlimited' /etc/security/limits.conf
RUN sed -i.bak '/\# End of file/ i\\*                soft    memlock         unlimited\n' /etc/security/limits.conf
RUN sed -i.bak '/\# End of file/ i\\*                hard    nofile          65536' /etc/security/limits.conf
RUN sed -i.bak '/\# End of file/ i\\*                soft    nofile          65536\n' /etc/security/limits.conf
RUN sed -i.bak '/\# end of pam-auth-update config/ i\\# Following line was added by docker-couchbase-server' /etc/pam.d/common-session
RUN sed -i.bak '/\# end of pam-auth-update config/ i\session    required        pam_limits.so\n' /etc/pam.d/common-session

RUN apt-get -y install librtmp0 libssl0.9.8 lsb-release

# sets root password to password, but isn't accessible from the outside
RUN echo 'mysql-server-5.5 mysql-server/root_password password password' | debconf-set-selections
RUN echo 'mysql-server-5.5 mysql-server/root_password_again password password' | debconf-set-selections

RUN apt-get install -y mysql-server --fix-missing --fix-broken && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

ENV HEMLOCK_PULLED_AT 2014-02-27
RUN git clone https://github.com/Lab41/Hemlock.git
RUN cd /Hemlock; python setup.py install

# kibana
RUN apt-get install -y zip
RUN wget http://download.elasticsearch.org/kibana/kibana/kibana-latest.zip
RUN unzip kibana-latest.zip
ADD config.js /kibana-latest/

# Download Couchbase Server package to /tmp & install
ADD $CB_DOWNLOAD_URL/$CB_VERSION/$CB_PACKAGE /tmp/$CB_PACKAGE
RUN dpkg -i /tmp/$CB_PACKAGE
RUN ln -s /opt/couchbase/bin/couchbase-cli /usr/local/bin/

# Put start script
ADD couchbase-start /usr/local/bin/

ADD . /src

# couchbase plugin with elasticsearch
RUN mkdir /usr/share/elasticsearch/plugins/transport-couchbase
RUN unzip -f /src/elasticsearch-transport-couchbase-1.1.0.zip -d /usr/share/elasticsearch/plugins/transport-couchbase 
RUN cp /src/couchbase_template.json /usr/share/elasticsearch/plugins/transport-couchbase/couchbase_template.json
RUN service elasticsearch stop

EXPOSE 8000 8080 9200 8091

CMD ["/bin/bash", "/src/startup.sh"]
