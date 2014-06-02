FROM lab41/dendrite-snap 
MAINTAINER Charlie Lewis <charliel@lab41.org>
 
RUN touch /var/log/tomcat7/catalina.out
EXPOSE 8000 8448 

# dev
ENV UPDATED 05-29-2014-0855
RUN mkdir /forks; cd forks; git clone https://github.com/cglewis/Dendrite.git; cd /forks/Dendrite; git checkout yarn; mvn package -f /forks/Dendrite/pom.xml -DskipTests; mv /forks/Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war

# add scripts and binaries
#RUN mkdir /tmp/dendrite; cp /forks/Dendrite/bin/bigclam /tmp/dendrite/bigclam; cp /forks/Dendrite/bin/graphgen /tmp/dendrite/graphgen; cp /forks/Dendrite/bin/create_graph.sh /tmp/dendrite/create_graph.sh; cp /forks/Dendrite/bin/snap.sh /tmp/dendrite/snap.sh


# run supervisord daemon
CMD /usr/bin/supervisord && tail -F /var/log/tomcat7/catalina.out
