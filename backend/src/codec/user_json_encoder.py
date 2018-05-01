import json


class UserJsonEncoder():

    def __init__(self, user, complete=False):
        self._user = user
        self._complete = complete

    def encode(self, format='string'):
        result = {}
        result['user_id'] = self._user.user_id
        result['name'] = self._user.name
        if self._complete:
            result['email'] = self._user.email
            result['phone'] = self._user.phone
            result['useemail'] = self._user.useemail
            result['profile'] = self._user.profile
            result['access'] = self._user.access
            result['validated'] = self._user.validated
            result['smsvalidated'] = self._user.smsvalidated
            result['lastlogin'] = self._user.lastlogin
            result['loginkey'] = self._user.loginkey
        if format == 'dict':
            return result
        return json.dumps(result)
