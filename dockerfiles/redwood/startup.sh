#!/bin/bash

/usr/sbin/mysqld &
sleep 5

echo "CREATE DATABASE redwood;" | mysql -uroot -ppassword
mysql -uroot -ppassword -Dredwood < /Redwood/sql/create_redwood_db.sql
mysql -uroot -ppassword -Dredwood < /Redwood/sql/create_redwood_sp.sql

# untar the data
cd /src; tar xfz data.tar.gz -C /Redwood/reports/output

ln -s /Redwood/reports/output /node_modules/tty.js/static/output

# start the tty webapp
/node_modules/tty.js/bin/tty.js --port 8000
