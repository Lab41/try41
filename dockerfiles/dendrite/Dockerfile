FROM lab41/dendrite-snap 
MAINTAINER Charlie Lewis <charliel@lab41.org>
 
RUN touch /var/log/tomcat7/catalina.out
EXPOSE 8000 8448 

# dev
ENV UPDATED 05-29-2014-0855
RUN mkdir /forks; cd forks; git clone https://github.com/cglewis/Dendrite.git; cd /forks/Dendrite; git checkout yarn; mvn package -f /forks/Dendrite/pom.xml -DskipTests; mv /forks/Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war

# add scripts and binaries
#RUN mkdir /tmp/dendrite; cp /forks/Dendrite/bin/bigclam /tmp/dendrite/bigclam; cp /forks/Dendrite/bin/graphgen /tmp/dendrite/graphgen; cp /forks/Dendrite/bin/create_graph.sh /tmp/dendrite/create_graph.sh; cp /forks/Dendrite/bin/snap.sh /tmp/dendrite/snap.sh

# add rsyslog
RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

# run supervisord daemon
CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; /etc/init.d/rsyslog start; logger started try41 container; /usr/bin/supervisord && tail -F /var/log/tomcat7/catalina.out
