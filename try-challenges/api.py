from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new', methods=["POST"])
def new():
    container_id = 1234
    container_port = 23567
    url="%s:%s" % ("hostname", container_port)

    return jsonify(
            url=url,
            port=container_port,
            hipache_port=80,
            id=container_id)

@app.route('/details/<url>')
def details(url):
    return render_template("details.html",url=url)

@app.route('/robot.txt')
def robot():
    return render_template("robot.html")

if __name__ == '__main__':
    import sys, os
    app.run(host="0.0.0.0")
