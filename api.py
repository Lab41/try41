from flask import Flask
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import render_template_string
from flask import request
from flask import send_from_directory
from flask import url_for
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user
from flask.ext.user import login_required
from flask.ext.user import SQLAlchemyAdapter
from flask.ext.user import UserManager
from flask.ext.user import UserMixin

from docker import client

import json
import os
import redis
import sys
import time
import uuid

# set defaults
IMAGE_NAME1 = "dendrite"
IMAGE_NAME2 = "redwood"
IMAGE_NAME3 = "hemlock"

DOCKER_HOST = "172.17.42.1"
DOMAIN = "127.0.0.1"
REDIS_HOST = "localhost"

REDIS_PORT=6379

# dendrite
EXPOSED_PORT1=8000
EXPOSED_PORT2=8448

# redwood
EXPOSED_PORT3=8000
EXPOSED_PORT4=8080

# hemlock
EXPOSED_PORT5=8000

r = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
c = client.Client(version="1.6", base_url='http://%s:4243' % DOCKER_HOST)

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'frifjawyeyshuwaHadrofluHujNar)gruRapEutthyThifjevyuphlevcumEurv6'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///username:password@server/users'
    CSRF_ENABLED = True

    # Configure session cookie
    SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = False
    SESSION_COOKIE_HTTPONLY = True

    # Configure Flask-Mail
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    USER_ENABLE_USERNAME         = True
    USER_ENABLE_CONFIRM_EMAIL    = True
    USER_ENABLE_CHANGE_USERNAME  = True
    USER_ENABLE_CHANGE_PASSWORD  = True
    USER_ENABLE_FORGOT_PASSWORD  = True
    USER_ENABLE_RETYPE_PASSWORD  = True
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except: pass

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Initialize Flask extensions
    babel = Babel(app)                              # Initialize Flask-Babel
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Display Login page or Profile page
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return redirect(url_for('profile_page'))
        else:
            return redirect(url_for('user.login'))

    # The '/profile' page requires a logged-in user
    @app.route('/profile')
    @login_required                                 # Use of @login_required decorator
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Profile Page{%endtrans%}</h2>
                <p> {%trans%}Hello{%endtrans%}
                    {{ current_user.username or current_user.email }},</p>
                <p> <a href="{{ url_for('user.change_username') }}">
                    {%trans%}Change username{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_password') }}">
                    {%trans%}Change password{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

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
        container = c.create_container(IMAGE_NAME1)
        container_id = container["Id"]
        c.start(container, publish_all_ports=True)
        b = c.inspect_container(container)
        url = store_metadata(exposed_ports, container_id, container, IMAGE_NAME1)
        return jsonify(url=url)

    @app.route('/new2', methods=["POST"])
    def new2():
        exposed_ports = [EXPOSED_PORT3]
        container = c.create_container(IMAGE_NAME2)
        container_id = container["Id"]
        c.start(container, publish_all_ports=True)
        b = c.inspect_container(container)
        url = store_metadata(exposed_ports, container_id, container, IMAGE_NAME2)
        return jsonify(url=url)

    @app.route('/new3', methods=["POST"])
    def new3():
        exposed_ports = [EXPOSED_PORT5]
        container = c.create_container(IMAGE_NAME3)
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
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
