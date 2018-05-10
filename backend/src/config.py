import json
import os


class Config(object):

    def __init__(self):
        data = {}
        if os.path.exists('/etc/mididec/config.json'):
            with open('/etc/mididec/config.json') as f:
                data = json.load(f)
        elif os.path.exists('../data/config.json'):
            with open('../data/config.json') as f:
                data = json.load(f)
        else:
            with open('config.json') as f:
                data = json.load(f)
        self._data = data

    @property
    def root(self):
        return self._data['root']

    @property
    def database(self):
        return self._data['database']['path']

    @property
    def sms_sid(self):
        return self._data['sms']['sid']

    @property
    def sms_token(self):
        return self._data['sms']['token']

    @property
    def email_server(self):
        return self._data['email']['server']

    @property
    def email_user(self):
        return self._data['email']['user']

    @property
    def email_password(self):
        return self._data['email']['password']
