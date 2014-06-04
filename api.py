from flask import Flask
from flask import g
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory

from docker import client

import json
import os
import redis
import sys
import time
import uuid

app = Flask(__name__)

# set defaults
IMAGE_NAME1 = "dendrite"
IMAGE_NAME2 = "redwood"
IMAGE_NAME3 = "hemlock"

DOCKER_HOST = "172.17.42.1"
DOMAIN = "127.0.0.1"
REDIS_HOST = "localhost"
RSYSLOG_HOST = "rsyslog"
PARENT_HOST = "parent"

REDIS_PORT=6379
DOCKER_PORT=4243

# dendrite
EXPOSED_PORT1=8000
EXPOSED_PORT2=8448

# redwood
EXPOSED_PORT3=8000
EXPOSED_PORT4=8080

# hemlock
EXPOSED_PORT5=8000

r = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
c = client.Client(version="1.6", base_url='http://%s:%s' % (DOCKER_HOST, DOCKER_PORT))

def store_metadata(exposed_ports, container_id, container, image_name):
    for exposed_port in exposed_ports:
        container_port = c.port(container_id, exposed_port)
        url = "%s:%s" % (DOMAIN, container_port)

    hmap = {}
    hmap['container_id'] = container_id
    hmap['container'] = container
    hmap['url'] = url
    hmap['timestamp'] = int(time.time())
    hmap['expired'] = 0
    hmap['image'] = image_name
    check_cookie()
    r.lpush(request.cookies.get('try41-uid'), json.dumps(hmap))
    return url

def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response

@app.before_request
def check_cookie():
    uid = request.cookies.get('try41-uid')
    if uid is None:
        uid = str(uuid.uuid4())
        @after_this_request
        def save_cookie(response):
            response.set_cookie('try41-uid', uid)
    
    r.sadd('sessions', uid)
    g.uid = uid

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/github-buttons')
def github_buttons():
    return render_template("github-btn.html")

@app.route('/new', methods=["POST"])
def new():
    exposed_ports = [EXPOSED_PORT1]
    container = c.create_container(IMAGE_NAME1, environment={'REMOTE_HOST': RSYSLOG_HOST, 'PARENT_HOST': PARENT_HOST})
    container_id = container["Id"]
    c.start(container, publish_all_ports=True)
    b = c.inspect_container(container)
    url = store_metadata(exposed_ports, container_id, container, IMAGE_NAME1)
    return jsonify(url=url)

@app.route('/new2', methods=["POST"])
def new2():
    exposed_ports = [EXPOSED_PORT3]
    container = c.create_container(IMAGE_NAME2, environment={'REMOTE_HOST': RSYSLOG_HOST, 'PARENT_HOST': PARENT_HOST})
    container_id = container["Id"]
    c.start(container, publish_all_ports=True)
    b = c.inspect_container(container)
    url = store_metadata(exposed_ports, container_id, container, IMAGE_NAME2)
    return jsonify(url=url)

@app.route('/new3', methods=["POST"])
def new3():
    exposed_ports = [EXPOSED_PORT5]
    container = c.create_container(IMAGE_NAME3, environment={'REMOTE_HOST': RSYSLOG_HOST, 'PARENT_HOST': PARENT_HOST})
    container_id = container["Id"]
    c.start(container, publish_all_ports=True)
    b = c.inspect_container(container)
    url = store_metadata(exposed_ports, container_id, container, IMAGE_NAME3)
    return jsonify(url=url)

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
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_REFRESH_EACH_REQUEST'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SECRET_KEY'] = 'secret'

    app.run(host="0.0.0.0")
