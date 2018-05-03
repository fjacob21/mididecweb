#!/usr/bin/python
from flask import Flask, jsonify, abort, request
from flask import Response, send_from_directory, redirect
from events import Events
from users import Users
from mailinglist import MailingList
from stores import SqliteStore
from codec import AttendeeJsonEncoder
from session import Session

store = SqliteStore()
application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'
events = Events(store)
users = Users(store)
mailinglist = MailingList(store)


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
    session = Session({}, events, users, request.args.get('loginkey'))
    return jsonify(session.get_events())


@application.route(api + 'events/<event_id>')
def get_event(event_id):
    session = Session({}, events, users, request.args.get('loginkey'))
    event_dict = session.get_event(event_id)
    if not event_dict:
        abort(400)
    return jsonify(event_dict)


@application.route(api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    session = Session({}, events, users, request.args.get('loginkey'))
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
    session = Session(request.json, events, users, request.args.get('loginkey'))
    event_dict = session.add_event()
    if not event_dict:
        abort(400)
    return jsonify(event_dict)


@application.route(api + 'events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    session = Session({}, events, users, request.args.get('loginkey'))
    result_dict = session.remove_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    result_dict = session.register_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/cancel_registration', methods=['POST'])
def cancel_registration(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    result_dict = session.unregistration(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    result_dict = session.publish_event(event_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'mailinglist')
def get_mailinglist():
    result = []
    for m in mailinglist.members:
        result.append(AttendeeJsonEncoder(m).encode())
    return jsonify({'mailinglist': result})


@application.route(api + 'mailinglist/register', methods=['POST'])
def register_mailinglist():
    if not request.json:
        abort(400)
    if "name" not in request.json or "email" not in request.json:
        abort(400)

    name = request.json["name"]
    email = request.json["email"]
    phone = ''
    if "phone" in request.json:
        phone = request.json["phone"]
    useemail = True
    if "useemail" in request.json:
        useemail = request.json["useemail"]
    usesms = False
    if "usesms" in request.json:
        usesms = request.json["usesms"]
    if mailinglist.find_member(email) != -1:
        abort(400)
    u = users.add(email, name, name, '', phone, useemail, usesms)
    res = mailinglist.register(u)
    return jsonify({'result': res})


@application.route(api + 'mailinglist/unregister', methods=['POST'])
def unregister_mailinglist():
    if not request.json:
        abort(400)
    if "email" not in request.json:
        abort(400)
    email = request.json["email"]
    if mailinglist.find_member(email) == -1:
        abort(400)
    res = mailinglist.unregister(email)
    return jsonify({'result': res})


@application.route(api + 'users', methods=['GET'])
def get_users():
    session = Session({}, events, users, request.args.get('loginkey'))
    return jsonify(session.get_userss())


@application.route(api + 'users', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    user_dict = session.add_user()
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    session = Session({}, events, users, request.args.get('loginkey'))
    user_dict = session.get_user(user_id)
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    user_dict = session.update_user(user_id)
    if not user_dict:
        abort(400)
    return jsonify(user_dict)


@application.route(api + 'users/<user_id>/login', methods=['POST'])
def login(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    result_dict = session.login(user_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'users/<user_id>/logout', methods=['POST'])
def logout(user_id):
    if not request.json:
        abort(400)
    session = Session(request.json, events, users, request.args.get('loginkey'))
    result_dict = session.logout(user_id)
    if not result_dict:
        abort(400)
    return jsonify(result_dict)


@application.route(api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    session = Session({}, events, users, request.args.get('loginkey'))
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
