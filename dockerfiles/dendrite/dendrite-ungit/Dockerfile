FROM lab41/dendrite-graphlab
MAINTAINER Charlie Lewis <charliel@lab41.org>

# ungit
RUN npm install -g grunt-cli
RUN sed "s|allowedDomains: 'http://localhost:8000',|allowedDomains: '*',|" -i /Dendrite/src/main/nodejs/ungit/source/config.js; \
    cd /Dendrite/src/main/nodejs/ungit; grunt --force
ADD npm.conf /etc/supervisor/conf.d/npm.conf
RUN sed 's|port="8080" protocol="HTTP/1.1"|port="8000" protocol="HTTP/1.1"|' -i /var/lib/tomcat7/conf/server.xml; \
    sed 's|<Connector port="8080" protocol="HTTP/1.1"|<Connector port="8000" protocol="HTTP/1.1"|' -i /var/lib/tomcat7/conf/server.xml; \
    rm -rf /Dendrite
