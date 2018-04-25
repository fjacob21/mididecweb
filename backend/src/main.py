#!/usr/bin/python
from flask import Flask, jsonify, abort, request, Response, send_from_directory, redirect
from events import Events
from users import Users
from icalgenerator import iCalGenerator
from mailinglist_member import MailingListMember
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from datetime import datetime, timedelta
from store import Store as OldStore
from stores import MemoryStore
from codec import UserJsonEncoder, EventJsonEncoder, EventsJsonEncoder

store = MemoryStore()
oldstore = OldStore()
oldstore.connect()
application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'
events = Events(store)
users = Users(store)
mailinglist = oldstore.restore_mailinglist()
oldstore.close()


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@application.before_request
def before_request():
    oldstore.connect()


@application.teardown_request
def teardown_request(exception):
    oldstore.close()


@application.route(api + 'events')
def get_events():
    return jsonify({'events': EventsJsonEncoder(events).encode('dict')})


@application.route(api + 'events/<event_id>')
def get_event(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    return jsonify({'event': EventJsonEncoder(e).encode('dict')})


@application.route(api + 'events/<event_id>/attendees')
def get_event_attendees(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    result = []
    for a in e.attendees:
        result.append(UserJsonEncoder(a).encode('dict'))
    return jsonify({'attendees': result})


@application.route(api + 'events/<event_id>/waitings')
def get_event_waiting(event_id):
    e = events.get(event_id)
    if not e:
        abort(400)
    result = []
    for a in e.waiting_attendees:
        result.append(UserJsonEncoder(a).encode('dict'))
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
    print(event_id, ev)
    if not ev:
        abort(400)
    events.remove(event_id)
    store.store_events(events)
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
    u = users.add(email, name, name, phone, useemail, usesms)
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
        result.append(UserJsonEncoder(m).encode())
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
    m = MailingListMember(name, email, phone, useemail, usesms)
    res = mailinglist.register(m)
    store.store_mailinglist(mailinglist)
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
    mailinglist.unregister(email)
    store.store_mailinglist(mailinglist)
    return jsonify({'result': True})


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
