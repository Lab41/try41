FROM lab41/dendrite-repos
MAINTAINER Charlie Lewis <charliel@lab41.org>

# ungit
RUN npm install -g grunt-cli
RUN sed "s|allowedDomains: 'http://localhost:8000',|allowedDomains: '*',|" -i /Dendrite/src/main/nodejs/ungit/source/config.js; \
    cd /Dendrite/src/main/nodejs/ungit; grunt --force
ADD npm.conf /etc/supervisor/conf.d/npm.conf
