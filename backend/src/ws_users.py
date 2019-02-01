from io import BytesIO
from config import Config
import errors
from flask import Blueprint, request, jsonify, send_file
from PIL import Image, ExifTags, ImageDraw, ImageOps
from session import Session
from session_exception import SessionError
import ws
import logger


config = Config()
users_page = Blueprint('users_page', __name__,
                        template_folder='templates')

@users_page.route(ws.api + 'users', methods=['GET'])
def get_users():
    logger.webapi().info('GET users - Get all users')
    session = Session({}, ws.get_store(), request.args.get('loginkey'), config,
                      ws.request_server())
    return jsonify(session.get_users())


@users_page.route(ws.api + 'users', methods=['POST'])
def add_user():
    logger.webapi().info('POST users - Add new user')
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.add_user())
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/validate', methods=['POST'])
def validate_user_info():
    logger.webapi().info('POST users/validate - Validate user')
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.validate_user_info())
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>', methods=['GET'])
def get_user(user_id):
    logger.webapi().info('GET users/{0} - Get user info'.format(user_id))
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return jsonify(session.get_user(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/avatar', methods=['GET'])
def get_user_avatar(user_id):
    logger.webapi().info('GET users/{0}/avatar - Get user avatar'.format(user_id))
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
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
            # r, g, b = img.split()
            # zeroimg = Image.new('L', img.size, color=0)
            # img = Image.merge("RGB", (r, zeroimg, zeroimg))
            size = (img.size[0], img.size[0]) #(128, 128)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            img = output
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/validate', methods=['GET'])
def get_user_validate(user_id):
    logger.webapi().info('GET users/{0}/validate - Get user validation'.format(user_id))
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return session.validate_user(user_id)
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/sendcode', methods=['POST'])
def send_user_code(user_id):
    logger.webapi().info('POST users/{0}/sendcode - Send user code'.format(user_id))
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return jsonify(session.sendcode(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/validatecode', methods=['POST'])
def validate_user_code(user_id):
    logger.webapi().info('POST users/{0}/validatecode - Validate user code'.format(user_id))
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return jsonify(session.validatecode(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>', methods=['POST'])
def update_user(user_id):
    logger.webapi().info('POST users/{0} - Update user info'.format(user_id))
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.update_user(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/avatar', methods=['POST'])
def update_user_avatar(user_id):
    logger.webapi().info('POST users/{0}/avatar - Change user avatar'.format(user_id))
    try:
        session = Session({}, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        file = request.files['avatar']
        return jsonify(session.update_user_avatar(user_id, file))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/login', methods=['POST'])
def login(user_id):
    logger.webapi().info('POST users/{0}/login - User login'.format(user_id))
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.login(user_id, request.remote_addr))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>/logout', methods=['POST'])
def logout(user_id):
    logger.webapi().info('POST users/{0}/logout - User logout'.format(user_id))
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.logout(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/<user_id>', methods=['DELETE'])
def rm_user(user_id):
    logger.webapi().info('DELETE users/{0} - Delete user'.format(user_id))
    try:
        params = {}
        if request.json:
            params = request.json
        session = Session(params, ws.get_store(), request.args.get('loginkey'),
                          config, ws.request_server())
        return jsonify(session.remove_user(user_id))
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/resetpsw', methods=['POST'])
def reset_user_password():
    logger.webapi().info('POST users/resetpsw - Send user reset password')
    try:
        if not request.json:
            return ws.return_error(errors.ERROR_INVALID_REQUEST)
        session = Session(request.json, ws.get_store(),
                          request.args.get('loginkey'), config,
                          request.url_root)
        return jsonify(session.reset_user_password())
    except SessionError as se:
        return ws.return_error(se.code)


@users_page.route(ws.api + 'users/resetpsw/validate', methods=['POST'])
def validate_reset_user_password():
    logger.webapi().info('POST users/resetpsw/validate - Validate user password reset code')
    if not request.json:
        return ws.return_error(errors.ERROR_INVALID_REQUEST)
    session = Session(request.json, ws.get_store(), request.args.get('loginkey'),
                      config, ws.request_server())
    return jsonify(session.validate_reset_user_password())


@users_page.route(ws.api + 'users/resetpsw/change', methods=['POST'])
def change_user_password():
    logger.webapi().info('POST users/resetpsw/change - Change user password')
    session = Session(request.json, ws.get_store(),
                      request.args.get('loginkey'), config,
                      request.url_root)
    return jsonify(session.change_user_password())