from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory


from docker import client

from os import environ

import redis

app = Flask(__name__)
app.debug = True

# set defaults
IMAGE_NAME1 = "172.17.42.1:80/dendrite"
IMAGE_NAME2 = "172.17.42.1:80/dendrite"
IMAGE_NAME3 = "172.17.42.1:80/dendrite"
DOMAIN = "localhost"
HIPACHE_PORT="80"
EXPOSED_PORT1="8080"
EXPOSED_PORT2="8080"
EXPOSED_PORT3="8080"

# environment variables, must be set in order for application to function
try:
    REDIS_PORT=environ["REDIS_PORT"]
    REDIS_HOST=environ["REDIS_HOST"]
    HIPACHE_PORT=environ["HIPACHE_PORT"]
    DOCKER_HOST=environ["DOCKER_HOST"]
except Exception, e:
    print e
    print "environment not properly configured"
    print environ
    import sys; sys.exit(1)

r = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
c = client.Client(base_url='http://%s:4243' % DOCKER_HOST)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new', methods=["POST"])
def new():
    container = c.create_container(IMAGE_NAME1, ports=[EXPOSED_PORT1])
    container_id = container["Id"]
    c.start(container_id)
    container_port = c.port(container_id, EXPOSED_PORT1)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), container_id)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), "http://%s:%s" %(DOMAIN, container_port))
    if HIPACHE_PORT == "80":
        url = "%s:%s" % (DOMAIN, container_port)
    else:
        url="%s:%s" % (DOMAIN, container_port)

    return jsonify(
            url=url,
            port=container_port,
            hipache_port=HIPACHE_PORT,
            id=container_id)

@app.route('/details/<url>')
def details(url):
    return render_template("details.html",url=url)

@app.route('/robot.txt')
def robot():
    return render_template("robot.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__ == '__main__':
    import sys, os
    app.run(host="0.0.0.0")
