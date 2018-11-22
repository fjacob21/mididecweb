import json


class AttendeeJsonEncoder():

    def __init__(self, attendee):
        self._attendee = attendee

    def encode(self, format='string'):
        result = {}
        result['user_id'] = self._attendee.user_id
        result['name'] = self._attendee.name
        result['alias'] = self._attendee.alias
        result['create_date'] = self._attendee.create_date
        result['have_avatar'] = self._attendee.avatar_path != ''
        result['phone'] = self._attendee.phone
        result['useemail'] = self._attendee.useemail
        result['usesms'] = self._attendee.usesms
        result['profile'] = self._attendee.profile
        result['validated'] = self._attendee.validated
        result['smsvalidated'] = self._attendee.smsvalidated
        result['lastlogin'] = self._attendee.lastlogin
        result['email'] = self._attendee.email
        result['loginkey'] = self._attendee.loginkey
        result['access'] = self._attendee.access
        result['present'] = self._attendee.present
        result['present_time'] = self._attendee.present_time

        if format == 'dict':
            return result
        return json.dumps(result)
