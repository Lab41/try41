from ubuntu:precise
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-04-08
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update

# supervisor
RUN apt-get install supervisor -y -q

# java
RUN apt-get install -y wget
RUN wget --quiet --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" -O jdk-7u51-linux-x64.tar.gz http://download.oracle.com/otn-pub/java/jdk/7u51-b13/jdk-7u51-linux-x64.tar.gz
RUN mkdir -p /usr/lib/jvm
RUN mv jdk-7u51-linux-x64.tar.gz /usr/lib/jvm
RUN tar zxvf /usr/lib/jvm/jdk-7u51-linux-x64.tar.gz -C /usr/lib/jvm
RUN update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk1.7.0_51/bin/javac 1
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.7.0_51/bin/java 1
RUN update-alternatives --set javac /usr/lib/jvm/jdk1.7.0_51/bin/javac
RUN update-alternatives --set java /usr/lib/jvm/jdk1.7.0_51/bin/java
RUN echo 'JAVA_HOME=/usr/lib/jvm/jdk1.7.0_51' >> /etc/profile
RUN echo 'PATH=$PATH:$JAVA_HOME/bin' >> /etc/profile
RUN echo 'export JAVA_HOME' >> /etc/profile
RUN echo 'export PATH' >> /etc/profile
ENV JAVA_HOME /usr/lib/jvm/jdk1.7.0_51
ENV PATH $PATH:$JAVA_HOME/bin

RUN apt-get install -y git maven
RUN apt-get install -y bzip2
RUN git clone https://github.com/Lab41/titan.git
RUN cd /titan; git checkout dendrite
RUN mvn install -f /titan/pom.xml -DskipTests
RUN git clone https://github.com/Lab41/faunus.git
RUN cd /faunus; git checkout dendrite
RUN sed -i 's/repo.aduna-software.org/repo.maven.apache.org/g' /faunus/pom.xml
RUN mvn install -f /faunus/pom.xml -DskipTests
RUN apt-get install -y tomcat7
RUN chmod -R 777 /var/lib
RUN git clone https://github.com/Lab41/Dendrite.git
RUN sed 's|<connectionUrl>scm:git:git@github.com:kylef-lab41/ungit.git</connectionUrl>|<connectionUrl>scm:git:https://github.com/kylef-lab41/ungit.git</connectionUrl>|' -i /Dendrite/pom.xml
RUN sed 's|" --graph " + exportDir;|" --graph " + exportDir.toString().substring(5)+"/part*";|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java
RUN sed 's|cmd += " --output " + importDir;|cmd += " --output " + importDir.toString().substring(5);|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java
RUN sed 's|cmd += " --saveprefix " + importDir;|cmd += " --saveprefix " + importDir.toString().substring(5);|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java
RUN cd /Dendrite; mvn scm:checkout -DwithGitHistoryServer=true
RUN sed 's/user: <FIXME.*>/user: "lab41"/' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js
RUN sed 's|local: <FIXME.*>|local: "/tmp/dendrite/history"|' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js
RUN sed 's|remote: <FIXME.*>|remote: "https://github.com"|' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js
RUN apt-get install -y python-software-properties
RUN apt-add-repository ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs
RUN npm install less
RUN cd /Dendrite/src/main/nodejs/ungit; git submodule update --init; npm install
RUN sed -i 's/0.4.2-dendrite-hadoop2-SNAPSHOT/0.4.1-Lab41-SNAPSHOT/g' /Dendrite/pom.xml
RUN mvn package -f /Dendrite/pom.xml -DskipTests
RUN cp /Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war
RUN sed 's/JAVA_OPTS="-Djava.awt.headless=true -Xmx128m -XX:+UseConcMarkSweepGC"/JAVA_OPTS="-Djava.awt.headless=true -Xmx1536m -XX:+UseConcMarkSweepGC -Dspring.profiles.active=prod -DwithGitHistoryServer=true"/' -i /etc/default/tomcat7
ADD tomcat.conf /etc/supervisor/conf.d/tomcat.conf
RUN mv faunus /var/lib/faunus
RUN mkdir /var/lib/tomcat7/dendrite
RUN cp /Dendrite/src/main/groovy/org/lab41/dendrite/dendrite-import.groovy /var/lib/tomcat7/dendrite/dendrite-import.groovy

# fix java due to tomcat installing java6
RUN unlink /usr/lib/jvm/default-java
RUN ln -s /usr/lib/jvm/jdk1.7.0_51 /usr/lib/jvm/default-java

# cdh4 package, key, and repo
ADD cdh4-repository_1.0_all.deb cdh4-repository_1.0_all.deb
RUN dpkg -i cdh4-repository_1.0_all.deb
RUN apt-get install -y curl
RUN curl -s http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh/archive.key | apt-key add -
RUN echo "deb [arch=amd64] http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib\ndeb-src http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib" > /etc/apt/sources.list.d/cloudera.list

RUN apt-get update

# zookeeper
RUN apt-get install -y zookeeper zookeeper-server
RUN service zookeeper-server init

# yarn
RUN apt-get install -y hadoop-mapreduce-historyserver hadoop-yarn-proxyserver hadoop-yarn-nodemanager hadoop-hdfs-datanode hadoop-mapreduce hadoop-yarn-resourcemanager hadoop-hdfs-namenode
ADD hadoop-mapreduce.conf /etc/supervisor/conf.d/hadoop-mapreduce.conf
ADD hadoop-yarn.conf /etc/supervisor/conf.d/hadoop-yarn.conf

# hbase
RUN apt-get install -y hbase-master
ADD hbase.conf /etc/supervisor/conf.d/hbase.conf
RUN echo 'export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_51' >> /etc/hbase/conf/hbase-env.sh

# format hdfs
RUN su -c "hadoop namenode -format" - hdfs

# elasticsearch
RUN apt-get install -y dpkg
RUN wget --no-check-certificate https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.5.deb
RUN dpkg -i elasticsearch-0.90.5.deb
RUN /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
RUN echo 'discovery.zen.ping.multicast.enabled: false' >> /etc/elasticsearch/elasticsearch.yml
RUN echo 'node.local: false' >> /etc/elasticsearch/elasticsearch.yml
RUN echo 'index.number_of_shards: 1' >> /etc/elasticsearch/elasticsearch.yml
RUN echo 'index.number_of_replicas: 0' >> /etc/elasticsearch/elasticsearch.yml
ADD elasticsearch.conf /etc/supervisor/conf.d/elasticsearch.conf

RUN chmod -R 777 /var/lib
RUN mkdir -p /usr/share/tomcat7/dendrite
RUN chmod -R 777 /usr/share/tomcat7/dendrite

# graphlab
RUN echo '127.0.0.1' >> /usr/share/tomcat7/graphlab_machine.txt
RUN cp /usr/share/tomcat7/graphlab_machine.txt /graphlab_machine.txt
RUN apt-get install -y gcc g++ build-essential libopenmpi-dev openmpi-bin default-jdk cmake zlib1g-dev git make
RUN git clone https://github.com/graphlab-code/graphlab.git
RUN cd graphlab; ./configure
RUN cd graphlab/release/toolkits/graph_analytics; make -j2
RUN cp -R /graphlab /usr/share/tomcat7/graphlab
ENV HADOOP_CONF_DIR /etc/hadoop/conf
RUN echo 'HADOOP_CONF_DIR=/etc/hadoop/conf' >> /etc/profile

# ssh for graphlab
ADD sshd.conf /etc/supervisor/conf.d/sshd.conf
RUN apt-get install openssh-server -y
RUN mkdir /var/run/sshd
RUN mkdir /var/log/ssh
RUN ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
ADD config /root/.ssh/config
RUN chown -R root:root /root/.ssh
RUN chmod 600 /root/.ssh/config

# ungit
RUN npm install -g grunt-cli
RUN sed "s|allowedDomains: 'http://localhost:8000',|allowedDomains: '*',|" -i /Dendrite/src/main/nodejs/ungit/source/config.js
RUN cd /Dendrite/src/main/nodejs/ungit; grunt --force
ADD npm.conf /etc/supervisor/conf.d/npm.conf
RUN sed 's|port="8080" protocol="HTTP/1.1"|port="8000" protocol="HTTP/1.1"|' -i /var/lib/tomcat7/conf/server.xml
RUN sed 's|<Connector port="8080" protocol="HTTP/1.1"|<Connector port="8000" protocol="HTTP/1.1"|' -i /var/lib/tomcat7/conf/server.xml

# snap
RUN apt-get install -y gnuplot
RUN wget --no-check-certificate https://snap.stanford.edu/releases/Snap-2.2.zip
RUN unzip Snap-2.2.zip
RUN cd Snap-2.2; make all
RUN cp -R /Snap-2.2 /var/lib/tomcat7/
 
EXPOSE 8000 

# run supervisord daemon
CMD ["/usr/bin/supervisord", "-n"]
