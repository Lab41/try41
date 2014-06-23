#!/bin/bash

cp /src/favicon.ico /node_modules/tty.js/static/favicon.ico
cp /src/index.html /node_modules/tty.js/static/index.html
cp /src/tty.js /node_modules/tty.js/bin/tty.js
chmod +x /node_modules/tty.js/bin/tty.js

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
