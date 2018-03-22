#!/usr/bin/python
from flask import Flask, jsonify, abort, request

application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'


@application.route(api + 'events')
def get_events():
    return jsonify({'events': []})


@application.route(api + 'events/<event>')
def get_event(event):
    return jsonify({'event': {}})


@application.route(api + 'events/<event>/ical')
def get_event_ical(event):
    return jsonify({'event': {}})


@application.route(api + 'events/<event>/sendemails', methods=['POST'])
def send_event_emails(event):
    return jsonify({'event': {}})


@application.route(api + 'events', methods=['POST'])
def add_event():
    return jsonify({'event': {}})


@application.route(api + 'events', methods=['DELETE'])
def rm_event():
    return jsonify({'event': {}})


@application.route(api + 'events/<event>/register', methods=['POST'])
def register_event(event):
    if not request.json:
        abort(400)
    return jsonify({'result': True})


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
