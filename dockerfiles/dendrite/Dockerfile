FROM lab41/dendrite-snap 
MAINTAINER Charlie Lewis <charliel@lab41.org>
 
RUN touch /var/log/tomcat7/catalina.out

# add rsyslog
RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

EXPOSE 8000 8448 

# run supervisord daemon
CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; /etc/init.d/rsyslog start; logger started dendrite container $PARENT_HOST; /usr/bin/supervisord && tail -F /var/log/tomcat7/catalina.out
