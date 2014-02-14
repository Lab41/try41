from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory

from docker import client

import redis

app = Flask(__name__)
app.debug = True

# set defaults
IMAGE_NAME1 = "dendrite"
IMAGE_NAME2 = "redwood"
IMAGE_NAME3 = "hemlock"

DOCKER_HOST="172.17.42.1"
DOMAIN = "localhost"
REDIS_HOST="localhost"
REDIS_PORT=6379
EXPOSED_PORT1=8080
EXPOSED_PORT2=8080
EXPOSED_PORT3=8080

r = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
c = client.Client(version="1.6", base_url='http://%s:4243' % DOCKER_HOST)

def store_metadata(exposed_ports, container_id, container):
    for exposed_port in exposed_ports:
        container_port = c.port(container_id, exposed_port)
        #r.rpush("frontend:%s.%s" % (container_id, DOMAIN), container_id)
        #r.rpush("frontend:%s.%s" % (container_id, DOMAIN), "http://%s:%s" %(DOMAIN, container_port))
        # !! TODO more than one url when there is more than one exposed_port
        url = "%s:%s" % (DOMAIN, container_port)

    hmap = {}
    hmap['container_id'] = container_id
    hmap['container'] = container
    hmap['url'] = url
    #r.hmset(url, hmap)
    return url

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new', methods=["POST"])
def new():
    exposed_ports = [EXPOSED_PORT1]
    container = c.create_container(IMAGE_NAME1)
    container_id = container["Id"]
    c.start(container, publish_all_ports=True)
    b = c.inspect_container(container)
    url = store_metadata(exposed_ports, container_id, container)
    return jsonify(url=url)

@app.route('/new2', methods=["POST"])
def new2():
    container = c.create_container(IMAGE_NAME2, ports=[EXPOSED_PORT2])
    container_id = container["Id"]
    c.start(container_id)
    container_port = c.port(container_id, EXPOSED_PORT2)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), container_id)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), "http://%s:%s" %(DOMAIN, container_port))
    url="%s:%s" % (DOMAIN, container_port)

    container = c.create_container(IMAGE_NAME3, ports=[EXPOSED_PORT3])
    container_id = container["Id"]
    c.start(container_id)
    container_port = c.port(container_id, EXPOSED_PORT3)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), container_id)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), "http://%s:%s" %(DOMAIN, container_port))
    url="%s:%s" % (DOMAIN, container_port)

    return jsonify(
            url=url,
            port=container_port,
            id=container_id)

@app.route('/new3', methods=["POST"])
def new3():
    container = c.create_container(IMAGE_NAME1, ports=[EXPOSED_PORT1])
    container_id = container["Id"]
    c.start(container_id)
    container_port = c.port(container_id, EXPOSED_PORT1)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), container_id)
    r.rpush("frontend:%s.%s" % (container_id, DOMAIN), "http://%s:%s" %(DOMAIN, container_port))
    url="%s:%s" % (DOMAIN, container_port)

    return jsonify(
            url=url,
            port=container_port,
            id=container_id)

@app.route('/details/<url>')
def details(url):
    return render_template("details.html",url=url)

@app.route('/details2/<url>')
def details2(url):
    return render_template("details2.html",url=url)

@app.route('/details3/<url>')
def details3(url):
    return render_template("details3.html",url=url)

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
