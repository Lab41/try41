FROM lab41/dendrite-snap 
MAINTAINER Charlie Lewis <charliel@lab41.org>
 
RUN touch /var/log/tomcat7/catalina.out

# install jq for parsing json
RUN wget http://stedolan.github.io/jq/download/linux64/jq
RUN chmod +x ./jq
RUN cp jq /usr/bin

# add rsyslog
RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf
RUN sed 's/\$PrivDropToUser syslog/#\$PrivDropToUser syslog/' -i /etc/rsyslog.conf
RUN sed 's/\$PrivDropToGroup syslog/#\$PrivDropToGroup syslog/' -i /etc/rsyslog.conf

ADD rsyslog.conf /etc/supervisor/conf.d/rsyslog.conf
ADD startup.sh /startup.sh
RUN rm /etc/supervisor/conf.d/tomcat.conf

EXPOSE 8000 8448 

# run supervisord daemon
CMD pwd; \
    printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; \
    /usr/bin/supervisord; \
    sleep 2; \
    logger started dendrite container $PARENT_HOST; \
    /startup.sh; \
    service tomcat7 start; \
    tail -F /var/log/tomcat7/catalina.out
