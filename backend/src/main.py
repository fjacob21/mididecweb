#!/usr/bin/python3
from bcrypt_hash import BcryptHash
from flask import Flask, send_from_directory, request, redirect
from users import Users
from user import USER_ACCESS_SUPER
from logs import Logs
from config import Config
from session_exception import SessionError
import os
import errors
from loggenerator import LogGenerator
import ws
from ws_logs import logs_page
from ws_events import events_page
from ws_users import users_page


config = Config()
application = Flask(__name__, static_url_path='')
application.register_blueprint(logs_page)
application.register_blueprint(events_page)
application.register_blueprint(users_page)

def init_folders():
    os.makedirs('../data', exist_ok=True)
    os.makedirs('../data/img', exist_ok=True)
    os.makedirs('../data/img/users', exist_ok=True)


def set_root():
    store = ws.get_store()
    users = Users(store)
    password = BcryptHash(config.root['password']).encrypt()
    if users.get(config.root['user_id']):
        root = users.get(config.root['user_id'])
        root.email = config.root['email']
        root.name = config.root['name']
        root.alias = config.root['alias']
        root.password = password
    else:
        root = users.add(config.root['email'], config.root['name'],
                         config.root['alias'], password, '', False, False,
                         access=USER_ACCESS_SUPER,
                         user_id=config.root['user_id'])
        root.validated = True
    store.close()


def add_users():
    store = ws.get_store()
    users = Users(store)
    config_users = config.users
    for user in config_users:
        password = BcryptHash(user['password']).encrypt()
        if users.get(user['user_id']):
            u = users.get(user['user_id'])
            u.email = user['email']
            u.name = user['name']
            u.alias = user['alias']
            u.password = password
            u.validated = True
        else:
            print('Add user', user['user_id'])
            u = users.add(user['email'], user['name'],
                            user['alias'], password, '', False, False,
                            access=USER_ACCESS_SUPER,
                            user_id=user['user_id'])
            u.validated = True
    store.close()


@application.before_request
def before_request():
    ip = request.remote_addr
    generator = LogGenerator(ip, request.user_agent.string)
    log = generator.generate()
    store = ws.get_store()
    logs = Logs(store)
    logs.add(log['ip'], log['os'], log['os_version'], log['browser'], log['browser_version'], log['continent'], log['is_eu'], log['country'], log['country_emoji'], log['region'], log['city'])


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


init_folders()
set_root()
add_users()

if __name__ == '__main__':
    ws.inDebug = True
    application.run(debug=True, host='0.0.0.0', port=5000)
