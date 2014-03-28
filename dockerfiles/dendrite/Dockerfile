from ubuntu:precise
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-03-27
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update

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

RUN apt-get install -y git
RUN apt-get install -y maven
RUN git clone https://github.com/Lab41/titan.git
RUN cd /titan; git checkout dendrite
RUN mvn install -f /titan/pom.xml -DskipTests
RUN git clone https://github.com/Lab41/faunus.git
RUN cd /faunus; git checkout dendrite
RUN mvn install -f /faunus/pom.xml -DskipTests
RUN apt-get install -y tomcat7
RUN chmod -R 777 /var/lib/tomcat7
RUN git clone https://github.com/Lab41/Dendrite.git
RUN mvn package -f /Dendrite/pom.xml
RUN cp /Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war
RUN sed 's/JAVA_OPTS="-Djava.awt.headless=true -Xmx128m -XX:+UseConcMarkSweepGC"/JAVA_OPTS="-Djava.awt.headless=true -Xmx1536m -XX:+UseConcMarkSweepGC"/' -i /etc/default/tomcat7

# fix java due to tomcat installing java6
RUN unlink /usr/lib/jvm/default-java
RUN ln -s /usr/lib/jvm/jdk1.7.0_51 /usr/lib/jvm/default-java

EXPOSE 8080

CMD service tomcat7 start && tail -F /var/log/tomcat7/catalina.out
