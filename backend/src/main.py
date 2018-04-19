#!/usr/bin/python
from flask import Flask, jsonify, abort, request, Response, send_from_directory, redirect
from attendee import Attendee
# from events import Events
from event import Event
from icalgenerator import iCalGenerator
# from mailinglist import MailingList
from mailinglist_member import MailingListMember
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from datetime import datetime, timedelta
from store import Store
from codec import UserJsonEncoder, EventJsonEncoder, EventsJsonEncoder

store = Store()
store.connect()
application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'
events = store.restore_events()
mailinglist = store.restore_mailinglist()
store.close()


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@application.before_request
def before_request():
    store.connect()


@application.teardown_request
def teardown_request(exception):
    store.close()


@application.route(api + 'events')
def get_events():
    return jsonify({'events': EventsJsonEncoder(events).encode('dict')})


@application.route(api + 'events/<uid>')
def get_event(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    return jsonify({'event': EventJsonEncoder(e).encode('dict')})


@application.route(api + 'events/<uid>/attendees')
def get_event_attendees(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    result = []
    for a in e.attendees:
        result.append(UserJsonEncoder(a).encode('dict'))
    return jsonify({'attendees': result})


@application.route(api + 'events/<uid>/waitings')
def get_event_waiting(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    result = []
    for a in e.waiting_attendees:
        result.append(UserJsonEncoder(a).encode('dict'))
    return jsonify({'waitings': result})


@application.route(api + 'events/<uid>/ical')
def get_event_ical(uid):
    e = events.get(uid)
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
    uid = ''
    if "uid" in request.json:
        uid = request.json["uid"]
    e = Event(title, desc, max_attendee, start, duration, location, organizer_name, organizer_email, uid)
    events.add(e)
    store.store_events(events)
    return jsonify({'result': True, 'event': e.json})


@application.route(api + 'events/<uid>', methods=['DELETE'])
def rm_event(uid):
    ev = events.get(uid)
    print(uid, ev)
    if not ev:
        abort(400)
    events.remove(uid)
    store.store_events(events)
    return jsonify({'result': True})


@application.route(api + 'events/<uid>/register', methods=['POST'])
def register_event(uid):
    ev = events.get(uid)
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
    a = Attendee(name, email, phone, useemail, usesms)
    res = ev.register_attendee(a)
    store.store_events(events)
    return jsonify({'result': res})


@application.route(api + 'events/<uid>/cancel_registration', methods=['POST'])
def cancel_registration(uid):
    ev = events.get(uid)
    if not ev:
        abort(400)
    if not request.json:
        abort(400)
    if "email" not in request.json:
        abort(400)
    email = request.json["email"]
    a = ev.cancel_registration(email)
    store.store_events(events)
    if a:
        return jsonify({'promotee': a.json})
    return jsonify({'promotee': None})


@application.route(api + 'events/<uid>/publish', methods=['POST'])
def publish_event(uid):
    ev = events.get(uid)
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
