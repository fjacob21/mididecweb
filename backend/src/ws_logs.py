from config import Config
from flask import Blueprint, request, jsonify
from session import Session
from session_exception import SessionError
import ws

config = Config()
logs_page = Blueprint('logs_page', __name__,
                        template_folder='templates')

@logs_page.route(ws.api + 'logs')
def get_logs():
    try:
        session = Session({}, ws.get_store(), request.args.get('loginkey'), config,
                          ws.request_server())
        return jsonify(session.get_logs())
    except SessionError as se:
        return ws.return_error(se.code)