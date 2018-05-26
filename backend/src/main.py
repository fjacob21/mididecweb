#!/usr/bin/python3
from bcrypt_hash import BcryptHash
from flask import Flask, jsonify, request, make_response
from flask import Response, send_from_directory, redirect
from events import Events
from users import Users
from user import USER_ACCESS_SUPER
from stores import SqliteStore
from session import Session
from config import Config
from session_exception import SessionError
import os
import errors

config = Config()
store = SqliteStore(config.database)
application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'
events = Events(store)
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
                     config.root['alias'], password, '', True, True,
                     access=USER_ACCESS_SUPER, user_id=config.root['user_id'])
    root.validated = True


def return_error(code):
    error = {}
    error['code'] = code
    resp = make_response(jsonify(error), 400)
    return resp


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@application.before_request
def before_request():
    store.open()


@application.teardown_request
def teardown_request(exception):
    store.close()


@application.route(api + 'events')
def get_events():
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    return jsonify(session.get_events())


@application.route(api + 'events/<event_id>')
def get_event(event_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        event_dict = session.get_event(event_id)
        return jsonify(event_dict)
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        return Response(
            session.get_event_ical(event_id),
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=event.ics"})
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/jinja')
def get_event_jinja(event_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        event_dict = session.get_event_jinja(event_id)
        return event_dict
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events', methods=['POST'])
def add_event():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.add_event())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>', methods=['POST'])
def update_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.update_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.remove_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.register_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/unregister',
                   methods=['POST'])
def unregister_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.unregister_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.publish_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users', methods=['GET'])
def get_users():
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    return jsonify(session.get_users())


@application.route(api + 'users', methods=['POST'])
def add_user():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.add_user())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/validate', methods=['POST'])
def validate_user_info():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.validate_user_info())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        return jsonify(session.get_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/avatar', methods=['GET'])
def get_user_avatar(user_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        avatar_path = session.get_user_avatar(user_id)
        print(avatar_path)
        return send_from_directory(os.path.dirname(avatar_path), os.path.basename(avatar_path))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/validate', methods=['GET'])
def get_user_validate(user_id):
    try:
        session = Session({}, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        return session.validate_user(user_id)
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.update_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/avatar', methods=['POST'])
def update_user_avatar(user_id):
    try:
        session = Session({}, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        file = request.files['avatar']
        return jsonify(session.update_user_avatar(user_id, file))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/login', methods=['POST'])
def login(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.login(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/logout', methods=['POST'])
def logout(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, events, users,
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.logout(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    try:
        params = {}
        if request.json:
            params = request.json
        session = Session(params, events, users, request.args.get('loginkey'),
                          config, request.url_root)
        return jsonify(session.remove_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
