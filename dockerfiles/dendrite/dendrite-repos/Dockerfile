FROM lab41/dendrite-java
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REPOS_PULLED 05-15-2014
RUN git clone https://github.com/Lab41/titan.git
RUN cd /titan; git checkout dendrite-hadoop2
RUN mvn install -f /titan/pom.xml -DskipTests
RUN rm -rf /titan
RUN git clone https://github.com/Lab41/faunus.git
RUN cd /faunus; git checkout dendrite-hadoop2
RUN mvn install -f /faunus/pom.xml -DskipTests
RUN chmod -R 777 /var/lib
RUN git clone https://github.com/Lab41/Dendrite.git
RUN sed 's|<connectionUrl>scm:git:git@github.com:kylef-lab41/ungit.git</connectionUrl>|<connectionUrl>scm:git:https://github.com/kylef-lab41/ungit.git</connectionUrl>|' -i /Dendrite/pom.xml; \
    sed 's|" --graph " + exportDir;|" --graph " + exportDir.toString().substring(5)+"/part*";|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java; \
    sed 's|cmd += " --output " + importDir;|cmd += " --output " + importDir.toString().substring(5);|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java; \
    sed 's|cmd += " --saveprefix " + importDir;|cmd += " --saveprefix " + importDir.toString().substring(5);|' -i /Dendrite/src/main/java/org/lab41/dendrite/services/analysis/GraphLabService.java
RUN cd /Dendrite; mvn scm:checkout -DwithGitHistoryServer=true
RUN sed 's/user: <FIXME.*>/user: "lab41"/' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js; \
    sed 's|local: <FIXME.*>|local: "/tmp/dendrite/history"|' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js; \
    sed 's|remote: <FIXME.*>|remote: "https://github.com"|' -i /Dendrite/src/main/nodejs/ungit/public/source/app.js; \
    sed -i "s/port:.*/port: parseInt(window.location.port)+1,/g" /Dendrite/src/main/webapp/js/app.js; \
    sed -i "s/host:.*/host: window.location.hostname,/g" /Dendrite/src/main/webapp/js/app.js; \
    sed 's/JAVA_OPTS="-Djava.awt.headless=true -Xmx128m -XX:+UseConcMarkSweepGC"/JAVA_OPTS="-Djava.awt.headless=true -Xmx1536m -XX:+UseConcMarkSweepGC -Dspring.profiles.active=prod -DwithGitHistoryServer=true"/' -i /etc/default/tomcat7
RUN npm install less
RUN cd /Dendrite/src/main/nodejs/ungit; git submodule update --init; npm install
RUN mvn package -f /Dendrite/pom.xml -DskipTests
RUN mv /Dendrite/target/dendrite-0.1.0.war /var/lib/tomcat7/webapps/dendrite.war
ADD tomcat.conf /etc/supervisor/conf.d/tomcat.conf
RUN mv faunus /var/lib/faunus
RUN mkdir /var/lib/tomcat7/dendrite
RUN mv /Dendrite/src/main/groovy/org/lab41/dendrite/dendrite-import.groovy /var/lib/tomcat7/dendrite/dendrite-import.groovy

# fix java due to tomcat installing java6
RUN unlink /usr/lib/jvm/default-java; \
    ln -s /usr/lib/jvm/jdk1.7.0_51 /usr/lib/jvm/default-java
