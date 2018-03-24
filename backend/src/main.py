#!/usr/bin/python
from flask import Flask, jsonify, abort, request
from attendee import Attendee
from events import Events
from event import Event
from datetime import datetime, timedelta
import pytz

application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'
events = Events()


def generate_event():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return Event("test", "test", 1, start, dur, 'test', 'test', 'test@test.com', 'test')


events.add(generate_event())


@application.route(api + 'events')
def get_events():
    result = []
    for ev in events.list:
        result.append(ev.json)
    return jsonify({'events': result})


@application.route(api + 'events/<uid>')
def get_event(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    return jsonify({'event': e.json})


@application.route(api + 'events/<uid>/attendees')
def get_event_attendeesl(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    result = []
    for a in e.attendees:
        result.append(a.json)
    return jsonify({'attendees': result})


@application.route(api + 'events/<uid>/waitings')
def get_event_waiting(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    result = []
    for a in e.waiting_attendees:
        result.append(a.json)
    return jsonify({'waitings': result})


@application.route(api + 'events/<uid>/ical')
def get_event_ical(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    return jsonify({'event': {}})


@application.route(api + 'events/<uid>/sendemails', methods=['POST'])
def send_event_emails(uid):
    e = events.get(uid)
    if not e:
        abort(400)
    return jsonify({'event': {}})


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
        organizer_name = request.json["deorganizer_namesc"]
    organizer_email = ''
    if "organizer_email" in request.json:
        organizer_email = request.json["organizer_email"]
    e = Event(title, desc, max_attendee, start, duration, location, organizer_name, organizer_email)
    events.add(e)
    return jsonify({'result': True, 'event': e.json})


@application.route(api + 'events/<uid>', methods=['DELETE'])
def rm_event(uid):
    ev = events.get(uid)
    if not ev:
        abort(400)
    events.remove(uid)
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
    sendremindemail = False
    if "sendremindemail" in request.json:
        sendremindemail = request.json["sendremindemail"]
    sendremindsms = False
    if "sendremindsms" in request.json:
        sendremindsms = request.json["sendremindsms"]
    a = Attendee(name, email, phone, sendremindemail, sendremindsms)
    res = ev.register_attendee(a)
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
    if a:
        return jsonify({'promotee': a.json})
    return jsonify({'promotee': None})


@application.route(api + 'mailinglist')
def get_mailinglist():
    return jsonify({'mailinglist': []})


@application.route(api + 'mailinglist/register', methods=['POST'])
def register_mailinglist():
    if not request.json:
        abort(400)
    return jsonify({'result': True})


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
