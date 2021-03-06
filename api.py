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

from docker import Client

import json
import os
import re
import redis
import sys
import time
import uuid

# set defaults
IMAGE_NAME1 = "lab41/gestalt"

DOMAIN = "127.0.0.1"
REDIS_HOST = "localhost"
RSYSLOG_HOST = "rsyslog"
PARENT_HOST = "parent"

COOKIE="try41-uid"

REDIS_PORT=6379

# use user accounts
USERS=False

# use ssl
SSL=False

# gestalt
EXPOSED_PORT1=8000

r = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
c = Client(version='auto', base_url='unix://var/run/docker.sock')

BAD = False
UUID4 = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'secret' # change for production
    CSRF_ENABLED = True
    if USERS:
        SQLALCHEMY_DATABASE_URI = 'postgresql' # change for production

    # Configure session cookie
    if not USERS:
        SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = False
    SESSION_COOKIE_HTTPONLY = True

    # Configure Flask-Mail
    if USERS:
        MAIL_SERVER   = 'smtp' # change for production
        MAIL_PORT     = 25
        MAIL_USE_SSL  = False
        MAIL_DEFAULT_SENDER = 'sender' # change for production

    # Configure Flask-User
    if USERS:
        USER_ENABLE_USERNAME         = True
        USER_ENABLE_CONFIRM_EMAIL    = True
        USER_ENABLE_CHANGE_USERNAME  = True
        USER_ENABLE_CHANGE_PASSWORD  = True
        USER_ENABLE_FORGOT_PASSWORD  = True
        USER_ENABLE_RETYPE_PASSWORD  = True
        USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
        USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

def create_app():
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask extensions
    if USERS:
        babel = Babel(app)
        db = SQLAlchemy(app)
        mail = Mail(app)

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
        db_adapter = SQLAlchemyAdapter(db,  User)
        user_manager = UserManager(db_adapter, app)

        # The '/profile' page requires a logged-in user
        @app.route('/profile')
        @login_required
        def profile():
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
        global BAD
        urlport = ""
        for exposed_port in exposed_ports:
            container_port = c.port(container_id, exposed_port)
            url = "%s:%s" % (DOMAIN, container_port[0]['HostPort'])
            urlport += url+","

        hmap = {}
        hmap['container_id'] = container_id
        hmap['container'] = container
        hmap['url'] = urlport[:-1]
        hmap['timestamp'] = int(time.time())
        hmap['expired'] = 0
        hmap['image'] = image_name
        data = json.dumps(hmap)
        check_cookie()
        # check cookie formatting, ensure that it exists in sessions
        # also check that it doesn't already exist
        if not BAD:
            cookie = request.cookies.get(COOKIE)
            if re.match(UUID4, cookie):
                if r.sismember('sessions', cookie):
                    r.lpush(cookie, data)
                else:
                    app.logger.info('invalid session')
                    BAD = True
            else:
                app.logger.info('invalid uuid')
                BAD = True

    def get_url(request):
        global BAD
        # this is validated with check_cookie before_request
        if not BAD:
            uid = request.cookies.get(COOKIE)
            container = r.lindex(uid, 0)
            container = json.loads(container)
            url = container['url']
            if "," in url:
                url_list = url.split(',')
                url = url_list[-1]
            return url
        else:
            return ""

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
        global BAD
        uid = request.cookies.get(COOKIE)
        if uid is None:
            uid = str(uuid.uuid4())
            @after_this_request
            def save_cookie(response):
                # validate uid formatting, and that it doesn't conflict
                if re.match(UUID4, uid):
                    if r.sismember('sessions', uid):
                        app.logger.info('uuid already exists')
                        BAD = True
                    else:
                        r.sadd('sessions', uid)
                        g.uid = uid
                        BAD = False
                        response.set_cookie(COOKIE, uid, httponly=True)
                else:
                    app.logger.info('invalid uuid')
                    BAD = True
                BAD = False

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/github-buttons')
    def github_buttons():
        return render_template("github-btn.html")

    @app.route('/details/wait')
    def wait():
        if SSL:
            return redirect("/gestalt", code=302)
        else:
            return render_template("wait.html")

    @app.route('/new', methods=["POST"])
    def new():
        if not USERS or current_user.is_authenticated():
            exposed_ports = [EXPOSED_PORT1]
            cookie = request.cookies.get(COOKIE)
            if re.match(UUID4, cookie):
                spinup = 1
                # check if this image has already been spun up for this session
                if r.exists(cookie):
                    # !! TODO error check
                    data = r.lrange(cookie, 0, -1)
                    for record in data:
                        jrec = json.loads(record)
                        if jrec['image'] == "lab41/gestalt":
                            if jrec['expired'] == 0:
                                app.logger.info('a gestalt container is already running for this session')
                                spinup = 0
                                return jsonify(url="wait")
                if spinup == 1:
                    host_config = c.create_host_config(publish_all_ports=True)
                    if SSL:
                        container = c.create_container(image=IMAGE_NAME1, host_config=host_config, environment={'REMOTE_HOST': RSYSLOG_HOST, 'PARENT_HOST': PARENT_HOST, 'SSL': "True"})
                    else:
                        container = c.create_container(image=IMAGE_NAME1, host_config=host_config, environment={'REMOTE_HOST': RSYSLOG_HOST, 'PARENT_HOST': PARENT_HOST})
                    c.start(container=container.get('Id'))
                    b = c.inspect_container(container)
                    bad = store_metadata(exposed_ports, container.get('Id'), container, IMAGE_NAME1)
                    if bad:
                        return render_template("index.html")
                    else:
                        return jsonify(url="launch")
                else:
                    return jsonify(url="wait")
        else:
            return jsonify(url="login")

    @app.route('/details/login')
    def details_login():
        return redirect(url_for('user.login'))

    @app.route('/details/launch')
    def details():
        if not USERS or current_user.is_authenticated():
            url = get_url(request)
            return render_template("details.html",url=url, USERS=USERS, SSL=SSL, DOMAIN=DOMAIN)
        else:
            return jsonify(url="login")

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
    app.run(host="0.0.0.0")
