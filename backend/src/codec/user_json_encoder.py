import json


class UserJsonEncoder():

    def __init__(self, user, complete=False, islogin=False):
        self._user = user
        self._complete = complete
        self._islogin = islogin

    def encode(self, format='string'):
        result = {}
        result['infotype'] = 'normal'
        if self._complete:
            result['infotype'] = 'complete'
        elif self._islogin:
            result['infotype'] = 'login'
        result['user_id'] = self._user.user_id
        result['name'] = self._user.name
        result['alias'] = self._user.alias
        result['create_date'] = self._user.create_date
        if self._complete:
            result['password'] = self._user.password
            result['phone'] = self._user.phone
            result['useemail'] = self._user.useemail
            result['usesms'] = self._user.usesms
            result['profile'] = self._user.profile
            result['validated'] = self._user.validated
            result['smsvalidated'] = self._user.smsvalidated
            result['lastlogin'] = self._user.lastlogin
        if self._complete or self._islogin:
            result['email'] = self._user.email
            result['loginkey'] = self._user.loginkey
            result['access'] = self._user.access

        if format == 'dict':
            return result
        return json.dumps(result)
