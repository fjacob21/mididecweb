#!/usr/bin/python
from bcrypt_hash import BcryptHash
from flask import Flask, jsonify, abort, request
from flask import Response, send_from_directory, redirect
from events import Events
from users import Users
from user import USER_ACCESS_SUPER
from stores import SqliteStore
from session import Session
from config import Config

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
    root = users.add(config.root['email'], config.root['name'], config.root['alias'],
                     password, '', True, True, access=USER_ACCESS_SUPER,
                     user_id=config.root['user_id'])
    root.validated = True


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
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    event_dict = session.get_event(event_id)
    if not event_dict:
        abort(400)
    return jsonify(event_dict)


@application.route(api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    ical = session.get_event_ical(event_id)
    if not ical:
        abort(400)
    return Response(
        ical,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=event.ics"})


@application.route(api + 'events', methods=['POST'])
def add_event():
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    event_dict = session.add_event()
    if not event_dict:
        abort(400)
    return jsonify(event_dict)


@application.route(api + 'events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    result_dict = session.remove_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    result_dict = session.register_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/unregister',
                   methods=['POST'])
def unregister_event(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    result_dict = session.unregister_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    result_dict = session.publish_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'users', methods=['GET'])
def get_users():
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    return jsonify(session.get_users())


@application.route(api + 'users', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    user_dict = session.add_user()
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/validate', methods=['POST'])
def validate_user_info():
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    validate_dict = session.validate_user_info()
    if not validate_dict:
        abort(400)
    return jsonify(validate_dict)


@application.route(api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    user_dict = session.get_user(user_id)
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/<user_id>/validate', methods=['GET'])
def get_user_validate(user_id):
    session = Session({}, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    validate_html = session.validate_user(user_id)
    if not validate_html:
        abort(400)
    return validate_html


@application.route(api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    user_dict = session.update_user(user_id)
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/<user_id>/login', methods=['POST'])
def login(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    result_dict = session.login(user_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'users/<user_id>/logout', methods=['POST'])
def logout(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users,
                      request.args.get('loginkey'), config, request.url_root)
    result_dict = session.logout(user_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    params = {}
    if request.json:
        params = request.json
    session = Session(params, events, users, request.args.get('loginkey'), config,
                      request.url_root)
    result_dict = session.remove_user(user_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
