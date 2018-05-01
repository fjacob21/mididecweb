#!/usr/bin/python
from flask import Flask, jsonify, abort, request, Response, send_from_directory, redirect
from events import Events
from users import Users, USER_ACCESS_SUPER, USER_ACCESS_MANAGER
from icalgenerator import iCalGenerator
from mailinglist import MailingList
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from datetime import datetime, timedelta
from stores import SqliteStore
from codec import AttendeeJsonEncoder, EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder

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
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    complete = False
    if loginkey and req_user and req_user.validate_access(USER_ACCESS_SUPER):
        complete = True
    result = EventsJsonEncoder(events, complete=complete).encode('dict')
    return jsonify({'events': result})


@application.route(api + 'events/<event_id>')
def get_event(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    complete = False
    if loginkey and req_user and req_user.validate_access(USER_ACCESS_SUPER):
        complete = True
    result = EventJsonEncoder(e, complete=complete).encode('dict')
    return jsonify({'event': result})


@application.route(api + 'events/<event_id>/attendees')
def get_event_attendees(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    complete = False
    if req_user:
        is_owner = (req_user.email == e.organizer_email and
                    req_user.validate_access(USER_ACCESS_MANAGER))
        is_admin = req_user.validate_access(USER_ACCESS_SUPER)
        if is_admin or is_owner:
            complete = True
    result = []
    for a in e.attendees:
        result.append(AttendeeJsonEncoder(a, complete=complete).encode('dict'))
    return jsonify({'attendees': result})


@application.route(api + 'events/<event_id>/waitings')
def get_event_waiting(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    complete = False
    if req_user:
        is_owner = (req_user.email == e.organizer_email and
                    req_user.validate_access(USER_ACCESS_MANAGER))
        is_admin = req_user.validate_access(USER_ACCESS_SUPER)
        if is_admin or is_owner:
            complete = True
    result = []
    for a in e.waiting_attendees:
        result.append(AttendeeJsonEncoder(a, complete=complete).encode('dict'))
    return jsonify({'waitings': result})


@application.route(api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    return Response(
        iCalGenerator(e).generate(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=event.ics"})


@application.route(api + 'events', methods=['POST'])
def add_event():
    if not request.json:
        abort(400)

    if "title" not in request.json or "desc" not in request.json:
        abort(400)

    title = request.json["title"]
    desc = request.json["desc"]
    max_attendee = None
    if "max_attendee" in request.json:
        max_attendee = request.json["max_attendee"]
    start = None
    if "start" in request.json:
        start = request.json["start"]
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
    duration = None
    if "duration" in request.json:
        duration = int(request.json["duration"])
        duration = timedelta(seconds=duration)
    location = ''
    if "location" in request.json:
        location = request.json["location"]
    organizer_name = ''
    if "organizer_name" in request.json:
        organizer_name = request.json["organizer_name"]
    organizer_email = ''
    if "organizer_email" in request.json:
        organizer_email = request.json["organizer_email"]
    event_id = ''
    if "event_id" in request.json:
        event_id = request.json["event_id"]
    e = events.add(title, desc, max_attendee, start, duration, location, organizer_name, organizer_email, event_id)
    return jsonify({'result': True, 'event': EventJsonEncoder(e).encode('dict')})


@application.route(api + 'events/<event_id>', methods=['DELETE'])
def rm_event(event_id):
    ev = events.get(event_id)
    if not ev:
        abort(400)
    events.remove(event_id)
    return jsonify({'result': True})


@application.route(api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    ev = events.get(event_id)
    if not ev:
        abort(400)
    if not request.json:
        abort(400)
    if "name" not in request.json or "email" not in request.json:
        abort(400)

    name = request.json["name"]
    email = request.json["email"]
    phone = ''
    if "phone" in request.json:
        phone = request.json["phone"]
    useemail = False
    if "useemail" in request.json:
        useemail = request.json["useemail"]
    usesms = False
    if "usesms" in request.json:
        usesms = request.json["usesms"]
    u = users.add(email, name, name, '', phone, useemail, usesms)
    res = ev.register_attendee(u)
    return jsonify({'result': res})


@application.route(api + 'events/<event_id>/cancel_registration', methods=['POST'])
def cancel_registration(event_id):
    ev = events.get(event_id)
    if not ev:
        abort(400)
    if not request.json:
        abort(400)
    if "email" not in request.json:
        abort(400)
    email = request.json["email"]
    u = ev.cancel_registration(email)
    if u:
        return jsonify({'promotee': u.json})
    return jsonify({'promotee': None})


@application.route(api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    ev = events.get(event_id)
    if not ev:
        abort(400)
    if not request.json:
        abort(400)
    if ("usr" not in request.json or "psw" not in request.json or
       'sid' not in request.json or 'token' not in request.json):
        abort(405)
    usr = request.json["usr"]
    psw = request.json["psw"]
    sid = request.json["sid"]
    token = request.json["token"]
    body = EventTextGenerator(ev, False).generate()
    res = True
    for m in mailinglist.members:
        if m.useemail and m.email:
            sender = EmailSender(usr, psw,
                                 m.email, ev.title, body)
            res = sender.send()
        if m.usesms and m.phone:
            sender = SmsSender(sid, token,
                               m.phone, ev.title, body)
            res = sender.send()
    return jsonify({'result': res})


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
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    print(loginkey, req_user)
    complete = False
    if req_user:
        is_admin = req_user.validate_access(USER_ACCESS_SUPER)
        if is_admin:
            complete = True
    result = UsersJsonEncoder(users, complete=complete).encode('dict')
    return jsonify({'users': result})


@application.route(api + 'users', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)
    if ('email' not in request.json or
        'name' not in request.json or
        'alias' not in request.json or
       'password' not in request.json):
        abort(400)
    email = request.json["email"]
    name = request.json["name"]
    alias = request.json["alias"]
    password = request.json["password"]
    phone = ''
    if 'phone' in request.json:
        phone = request.json['phone']
    useemail = True
    if 'useemail' in request.json:
        useemail = request.json['useemail']
    usesms = False
    if 'usesms' in request.json:
        usesms = request.json['usesms']
    profile = ''
    if 'profile' in request.json:
        profile = request.json['profile']
    user = users.add(email, name, alias, password, phone, useemail, usesms, profile)
    result = UserJsonEncoder(user, complete=True).encode('dict')
    return jsonify({'result': result})


@application.route(api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    loginkey = request.args.get('loginkey')
    req_user = users.find_loginkey(loginkey)
    user = users.find_email(user_id)
    if not user:
        user = users.get(user_id)
    if not user:
        abort(400)
    complete = False
    if req_user:
        is_admin = req_user.validate_access(USER_ACCESS_SUPER)
        is_own = req_user == user
        if is_admin or is_own:
            complete = True
    result = UserJsonEncoder(user, complete=complete).encode('dict')
    return jsonify({'user': result})


@application.route(api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    return jsonify({'result': request.args})


@application.route(api + 'users/login', methods=['POST'])
def login_user():
    if not request.json:
        abort(400)
    if "user_id" not in request.json or "password" not in request.json:
        abort(400)
    user_id = request.json["user_id"]
    password = request.json["password"]
    loginkey = users.login(user_id, password)

    return jsonify({'loginkey': loginkey})


@application.route(api + 'users/logout', methods=['POST'])
def logout_user():
    if not request.json:
        abort(400)
    if "loginkey" not in request.json:
        abort(400)
    loginkey = request.json["loginkey"]
    result = users.logout(loginkey)

    return jsonify({'result': result})


@application.route(api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    result = False
    if not request.json:
        abort(400)
    if "loginkey" not in request.json:
        abort(400)
    loginkey = request.json["loginkey"]
    req_user = users.find_loginkey(loginkey)
    user = users.find_email(user_id)
    if not user:
        user = users.get(user_id)
    if not user:
        abort(400)
    if req_user == user or req_user.validate_access(USER_ACCESS_SUPER):
        users.remove(user.user_id)
    return jsonify({'result': result})


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
