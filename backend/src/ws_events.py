from config import Config
import errors
from flask import Blueprint, request, jsonify, Response, send_from_directory
import os
from session import Session
from session_exception import SessionError
import ws

config = Config()
events_page = Blueprint('events_page', __name__,
                        template_folder='templates')

@events_page.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@events_page.route(ws.api + 'events')
def get_events():
    session = Session({}, ws.get_store(), request.args.get('loginkey'), config,
                      ws.request_server())
    return jsonify(session.get_events())


@events_page.route(ws.api + 'events/<event_id>/presences')
def get_event_presences(event_id):
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return session.get_event_presences(event_id)
        return Response(
            session.get_event_presences(event_id),
            mimetype="events_page/pdf",
            headers={"Content-disposition":
                     "attachment; filename=presences.pdf"})
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>')
def get_event(event_id):
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        event_dict = session.get_event(event_id)
        return jsonify(event_dict)
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return Response(
            session.get_event_ical(event_id),
            mimetype="text/calendar",
            headers={"Content-disposition":
                     "attachment; filename=event.ics"})
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/jinja')
def get_event_jinja(event_id):
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        event_dict = session.get_event_jinja(event_id)
        return event_dict
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events', methods=['POST'])
def add_event():
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.add_event())
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>', methods=['POST'])
def update_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.update_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.remove_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.register_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/unregister',
                   methods=['POST'])
def unregister_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.unregister_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/present', methods=['POST'])
def present_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.present_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)

@events_page.route(ws.api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.publish_event(event_id))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/attachments/<attachment>', methods=['GET'])
def get_event_attachment(event_id, attachment):
    try:
        session = Session({}, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        print('get attachment', attachment)
        attachment_path = session.get_event_attachment(event_id, attachment)
        return send_from_directory(os.path.dirname(attachment_path),
                                   os.path.basename(attachment_path),
                                   as_attachment=True)
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/attachments', methods=['POST'])
def add_event_attachment(event_id):
    try:
        session = Session({}, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        attachment = request.files['attachment']
        return jsonify(session.add_event_attachment(event_id, attachment))
    except SessionError as se:
        return ws.return_error(se.code)


@events_page.route(ws.api + 'events/<event_id>/attachments', methods=['DELETE'])
def delete_event_attachment(event_id):
    try:
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.remove_event_attachment(event_id))
    except SessionError as se:
        return ws.return_error(se.code)