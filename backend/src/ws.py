from config import Config
from flask import Flask, jsonify, request, make_response
from stores import SqliteStore

config = Config()
api = '/mididec/api/v1.0/'
inDebug = False

def get_store():
    return SqliteStore(config.database)


def return_error(code):
    error = {}
    error['code'] = code
    resp = make_response(jsonify(error), 400)
    return resp

def request_server():
    if inDebug:
        return request.url_root + 'html/'
    return request.url_root