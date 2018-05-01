import json


class AttendeeJsonEncoder():

    def __init__(self, user, complete=False):
        self._user = user
        self._complete = complete

    def encode(self, format='string'):
        result = {}
        result['name'] = self._user.name
        if self._complete:
            result['email'] = self._user.email
            result['phone'] = self._user.phone
            result['useemail'] = self._user.useemail
            result['usesms'] = self._user.usesms
        if format == 'dict':
            return result
        return json.dumps(result)
