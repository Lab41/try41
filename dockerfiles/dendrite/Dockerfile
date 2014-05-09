from ubuntu:precise
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-05-08
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update --fix-missing
RUN apt-get install -y python-software-properties
RUN apt-add-repository ppa:chris-lea/node.js
RUN apt-get update

RUN apt-get install -y -q wget \
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

# java
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

ENV REPOS_UPDATED_AT 2014-05-08
RUN git clone https://github.com/Lab41/titan.git
RUN cd /titan; git checkout dendrite-hadoop2
RUN mvn install -f /titan/pom.xml -DskipTests
RUN git clone https://github.com/Lab41/faunus.git
RUN cd /faunus; git checkout dendrite-hadoop2
RUN mvn install -f /faunus/pom.xml -DskipTests
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
RUN npm install less
RUN cd /Dendrite/src/main/nodejs/ungit; git submodule update --init; npm install
RUN sed -i "s/port:.*/port: parseInt(window.location.port)+1,/g" /Dendrite/src/main/webapp/js/app.js
RUN sed -i "s/host:.*/host: window.location.hostname,/g" /Dendrite/src/main/webapp/js/app.js
RUN mvn package -f /Dendrite/pom.xml -DskipTests
RUN mv /Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war
RUN sed 's/JAVA_OPTS="-Djava.awt.headless=true -Xmx128m -XX:+UseConcMarkSweepGC"/JAVA_OPTS="-Djava.awt.headless=true -Xmx1536m -XX:+UseConcMarkSweepGC -Dspring.profiles.active=prod -DwithGitHistoryServer=true"/' -i /etc/default/tomcat7
ADD tomcat.conf /etc/supervisor/conf.d/tomcat.conf
RUN mv faunus /var/lib/faunus
RUN mkdir /var/lib/tomcat7/dendrite
RUN mv /Dendrite/src/main/groovy/org/lab41/dendrite/dendrite-import.groovy /var/lib/tomcat7/dendrite/dendrite-import.groovy

# fix java due to tomcat installing java6
RUN unlink /usr/lib/jvm/default-java
RUN ln -s /usr/lib/jvm/jdk1.7.0_51 /usr/lib/jvm/default-java

# cdh5 package, key, and repo
ADD cdh5-repository_1.0_all.deb cdh5-repository_1.0_all.deb
RUN dpkg -i cdh5-repository_1.0_all.deb
RUN curl -s http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh/archive.key | apt-key add -
RUN echo "deb [arch=amd64] http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh precise-cdh5 contrib\ndeb-src http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh precise-cdh5 contrib" > /etc/apt/sources.list.d/cloudera.list
RUN apt-get update

# zookeeper
RUN apt-get install -y zookeeper zookeeper-server
RUN service zookeeper-server init
ADD zookeeper.conf /etc/supervisor/conf.d/zookeeper.conf

# hdfs supervisor
ADD hadoop-hdfs-namenode.conf /etc/supervisor/conf.d/hadoop-hdfs-namenode.conf
ADD hadoop-hdfs-datanode.conf /etc/supervisor/conf.d/hadoop-hdfs-datanode.conf

# yarn
RUN apt-get install -y hadoop-mapreduce-historyserver hadoop-yarn-proxyserver hadoop-yarn-nodemanager hadoop-hdfs-datanode hadoop-mapreduce hadoop-yarn-resourcemanager hadoop-hdfs-namenode
ADD hadoop-mapreduce.conf /etc/supervisor/conf.d/hadoop-mapreduce.conf
ADD hadoop-yarn-nodemanager.conf /etc/supervisor/conf.d/hadoop-yarn-nodemanager.conf
ADD hadoop-yarn-resourcemanager.conf /etc/supervisor/conf.d/hadoop-yarn-resourcemanager.conf
RUN sed -i 's|</configuration>|<property><name>yarn.nodemanager.resource.memory-mb</name><value>8192</value></property></configuration>|' /etc/hadoop/conf/yarn-site.xml

# hbase
RUN apt-get install -y hbase-master hbase-regionserver
ADD hbase-master.conf /etc/supervisor/conf.d/hbase-master.conf
ADD hbase-regionserver.conf /etc/supervisor/conf.d/hbase-regionserver.conf
RUN echo 'export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_51' >> /etc/hbase/conf/hbase-env.sh
RUN sed -i 's|<configuration>|<configuration><property><name>hbase.cluster.distributed</name><value>true</value></property><property><name>hbase.rootdir</name><value>hdfs://localhost:54310/hbase</value></property>|' /etc/hbase/conf/hbase-site.xml

# add hdfs config
RUN sed -i 's|<configuration>|<configuration><property><name>fs.default.name</name><value>hdfs://localhost:54310/</value><description>.</description></property>|' /etc/hadoop/conf/core-site.xml

# format hdfs
RUN su -c "hadoop namenode -format" - hdfs
RUN service hadoop-hdfs-namenode start; service hadoop-hdfs-datanode start; su -c "hadoop fs -mkdir /user" - hdfs; su -c "hadoop fs -mkdir /user/root" - hdfs; su -c "hadoop fs -mkdir /user/root/dendrite" - hdfs; su -c "hadoop fs -chown -R root:root /user/root" - hdfs; su -c "hadoop fs -mkdir /tmp" - hdfs; su -c "hadoop fs -mkdir /hbase" - hdfs; su -c "hadoop fs -chown hbase /hbase" - hdfs; su -c "hadoop fs -chmod -R 777 /tmp" - hdfs 

# elasticsearch
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
RUN mv /usr/share/tomcat7/graphlab_machine.txt /graphlab_machine.txt
RUN git clone https://github.com/graphlab-code/graphlab.git
RUN cd graphlab; ./configure
RUN cd graphlab/release/toolkits/graph_analytics; make -j1
RUN mv /graphlab /usr/share/tomcat7/graphlab
ENV HADOOP_CONF_DIR /etc/hadoop/conf
RUN echo 'HADOOP_CONF_DIR=/etc/hadoop/conf' >> /etc/profile

# ssh for graphlab
ADD sshd.conf /etc/supervisor/conf.d/sshd.conf
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
RUN wget --no-check-certificate https://snap.stanford.edu/releases/Snap-2.2.zip
RUN unzip Snap-2.2.zip
RUN cd Snap-2.2; make all
RUN mv /Snap-2.2 /usr/share/tomcat7/
 
EXPOSE 8000 8448 

# run supervisord daemon
CMD ["/usr/bin/supervisord", "-n"]
