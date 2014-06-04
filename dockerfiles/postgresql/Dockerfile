FROM ubuntu:trusty
MAINTAINER Charlie Lewis <charliel@lab41.org>

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update

RUN apt-get -y -q install python-software-properties software-properties-common
RUN apt-get -y -q install postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

USER postgres

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker users

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

EXPOSE 5432

USER root

RUN sed 's/#\$ModLoad imudp/\$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#\$UDPServerRun 514/\$UDPServerRun 514/' -i /etc/rsyslog.conf

CMD printf "*.*\t@$REMOTE_HOST" >> /etc/rsyslog.d/50-default.conf; /etc/init.d/rsyslog start; logger started postgresql container; su -c "/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf" - postgres

