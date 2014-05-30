FROM lab41/dendrite-elasticsearch
MAINTAINER Charlie Lewis <charliel@lab41.org>

# graphlab
RUN echo '127.0.0.1' >> /usr/share/tomcat7/graphlab_machine.txt;
    mv /usr/share/tomcat7/graphlab_machine.txt /graphlab_machine.txt
RUN git clone https://github.com/graphlab-code/graphlab.git
RUN cd graphlab; ./configure
RUN cd graphlab/release/toolkits/graph_analytics; make -j1
RUN mkdir -p /usr/share/tomcat7/graphlab/release/toolkits; \
    cp /graphlab/release/toolkits/graph_analytics /usr/share/tomcat7/graphlab/release/toolkits/
ENV HADOOP_CONF_DIR /etc/hadoop/conf
RUN echo 'HADOOP_CONF_DIR=/etc/hadoop/conf' >> /etc/profile

# ssh for graphlab
ADD sshd.conf /etc/supervisor/conf.d/sshd.conf
RUN mkdir /var/run/sshd; mkdir /var/log/ssh; \
    ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa; \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
ADD config /root/.ssh/config
RUN chown -R root:root /root/.ssh; chmod 600 /root/.ssh/config
