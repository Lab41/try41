FROM lab41/dendrite-snap 
MAINTAINER Charlie Lewis <charliel@lab41.org>
 
RUN touch /var/log/tomcat7/catalina.out
EXPOSE 8000 8448 

# run supervisord daemon
CMD /usr/bin/supervisord && tail -F /var/log/tomcat7/catalina.out
