import json
import os


class Config(object):

    def __init__(self):
        self._path = self.find_config_file()

    def find_config_file(self):
        if os.path.exists('/etc/mididec/config.json'):
            return '/etc/mididec/config.json'
        elif os.path.exists('../data/config.json'):
            return '../data/config.json'
        return 'config.json'

    def load_config_file(self):
        data = {}
        with open(self._path) as f:
            data = json.load(f)
        return data

    @property
    def users(self):
        return self.load_config_file()['users']

    @property
    def root(self):
        return self.load_config_file()['root']

    @property
    def database(self):
        return self.load_config_file()['database']['path']

    @property
    def sms_sid(self):
        return self.load_config_file()['sms']['sid']

    @property
    def sms_token(self):
        return self.load_config_file()['sms']['token']

    @property
    def email_server(self):
        return self.load_config_file()['email']['server']

    @property
    def email_user(self):
        return self.load_config_file()['email']['user']

    @property
    def email_password(self):
        return self.load_config_file()['email']['password']
