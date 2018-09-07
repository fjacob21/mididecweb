#!/usr/bin/python3
import datetime
from bcrypt_hash import BcryptHash
from flask import Flask, jsonify, request, make_response
from flask import Response, send_from_directory, redirect, send_file
from users import Users
from user import USER_ACCESS_SUPER
from logs import Logs
from stores import SqliteStore
from session import Session
from config import Config
from session_exception import SessionError
import os
import errors
from loggenerator import LogGenerator
from PIL import Image, ExifTags
from io import BytesIO


inDebug = False
os.makedirs('../data', exist_ok=True)
os.makedirs('../data/img', exist_ok=True)
os.makedirs('../data/img/users', exist_ok=True)
config = Config()
application = Flask(__name__, static_url_path='')
api = '/mididec/api/v1.0/'


def set_root():
    store = get_store()
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


def get_store():
    return SqliteStore(config.database)


def return_error(code):
    error = {}
    error['code'] = code
    resp = make_response(jsonify(error), 400)
    return resp


@application.before_request
def before_request():
    ip = request.remote_addr
    generator = LogGenerator(ip, request.user_agent.string)
    log = generator.generate()
    store = get_store()
    logs = Logs(store)
    logs.add(log['ip'], log['os'], log['os_version'], log['browser'], log['browser_version'], log['continent'], log['is_eu'], log['country'], log['country_emoji'], log['region'], log['city'])


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@application.route(api + 'events')
def get_events():
    session = Session({}, get_store(), request.args.get('loginkey'), config,
                      request_server())
    return jsonify(session.get_events())


@application.route(api + 'events/<event_id>')
def get_event(event_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        event_dict = session.get_event(event_id)
        return jsonify(event_dict)
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/ical')
def get_event_ical(event_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return Response(
            session.get_event_ical(event_id),
            mimetype="text/calendar",
            headers={"Content-disposition":
                     "attachment; filename=event.ics"})
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/jinja')
def get_event_jinja(event_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        event_dict = session.get_event_jinja(event_id)
        return event_dict
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events', methods=['POST'])
def add_event():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.add_event())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>', methods=['POST'])
def update_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.update_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.remove_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/register', methods=['POST'])
def register_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.register_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/unregister',
                   methods=['POST'])
def unregister_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.unregister_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/publish', methods=['POST'])
def publish_event(event_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.publish_event(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/attachments/<attachment>', methods=['GET'])
def get_event_attachment(event_id, attachment):
    try:
        session = Session({}, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        print('get attachment', attachment)
        attachment_path = session.get_event_attachment(event_id, attachment)
        return send_from_directory(os.path.dirname(attachment_path),
                                   os.path.basename(attachment_path),
                                   as_attachment=True)
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/attachments', methods=['POST'])
def add_event_attachment(event_id):
    try:
        session = Session({}, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        attachment = request.files['attachment']
        return jsonify(session.add_event_attachment(event_id, attachment))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'events/<event_id>/attachments', methods=['DELETE'])
def delete_event_attachment(event_id):
    try:
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.remove_event_attachment(event_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users', methods=['GET'])
def get_users():
    session = Session({}, get_store(), request.args.get('loginkey'), config,
                      request_server())
    return jsonify(session.get_users())


@application.route(api + 'users', methods=['POST'])
def add_user():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.add_user())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/validate', methods=['POST'])
def validate_user_info():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.validate_user_info())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return jsonify(session.get_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/avatar', methods=['GET'])
def get_user_avatar(user_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        avatar_path = session.get_user_avatar(user_id)
        sizex = request.args.get('sizex')
        sizey = request.args.get('sizey')
        filter = request.args.get('filter')
        img = Image.open(avatar_path)
        if '_getexif' in dir(img) and img._getexif():
            exif = [(ExifTags.TAGS[k], v) for k, v in img._getexif().items()
                    if k in ExifTags.TAGS]
            if 'Orientation' not in exif:
                img = img
            elif exif['Orientation'] == 3:
                img = img.rotate(180, expand=True)
            elif exif['Orientation'] == 6:
                img = img.rotate(270, expand=True)
            elif exif['Orientation'] == 8:
                img = img.rotate(90, expand=True)
        if sizex and sizey:
            img.thumbnail((int(sizex), int(sizey)))
        if filter:
            r, g, b = img.split()
            zeroimg = Image.new('L', img.size, color=0)
            img = Image.merge("RGB", (r, zeroimg, zeroimg))
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/validate', methods=['GET'])
def get_user_validate(user_id):
    try:
        session = Session({}, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return session.validate_user(user_id)
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/sendcode', methods=['POST'])
def send_user_code(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return jsonify(session.sendcode(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/validatecode', methods=['POST'])
def validate_user_code(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return jsonify(session.validatecode(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.update_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/avatar', methods=['POST'])
def update_user_avatar(user_id):
    try:
        session = Session({}, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        file = request.files['avatar']
        return jsonify(session.update_user_avatar(user_id, file))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/login', methods=['POST'])
def login(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.login(user_id, request.remote_addr))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>/logout', methods=['POST'])
def logout(user_id):
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request_server())
        return jsonify(session.logout(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    try:
        params = {}
        if request.json:
            params = request.json
        session = Session(params, get_store(), request.args.get('loginkey'),
                          config, request_server())
        return jsonify(session.remove_user(user_id))
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/resetpsw', methods=['POST'])
def reset_user_password():
    try:
        if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, get_store(),
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.reset_user_password())
    except SessionError as se:
        return return_error(se.code)


@application.route(api + 'users/resetpsw/validate', methods=['POST'])
def validate_reset_user_password():
    if not request.json:
        return return_error(errors.ERROR_INVALID_REQUEST)
    session = Session(request.json, get_store(), request.args.get('loginkey'),
                      config, request_server())
    return jsonify(session.validate_reset_user_password())


@application.route(api + 'users/resetpsw/change', methods=['POST'])
def change_user_password():
    session = Session(request.json, get_store(),
                      request.args.get('loginkey'), config,
                      request.url_root)
    return jsonify(session.change_user_password())


@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/', path)


@application.route('/')
def root():
    return redirect('/html/index.html')


def request_server():
    if inDebug:
        return request.url_root + 'html/'
    return request.url_root


set_root()

if __name__ == '__main__':
    inDebug = True
    application.run(debug=True, host='0.0.0.0', port=5000)
