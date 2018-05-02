import json
from .user_json_encoder import UserJsonEncoder


class UsersJsonEncoder():

    def __init__(self, users, complete=False):
        self._users = users
        self._complete = complete

    def encode(self, format='string'):
        result = {}
        result['count'] = self._users.count
        events = []
        for user in self._users.list:
            events.append(UserJsonEncoder(user, self._complete).encode('dict'))
        result['users'] = events
        if format == 'dict':
            return result
        return json.dumps(result)
