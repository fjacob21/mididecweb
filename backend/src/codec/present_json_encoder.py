import json


class PresentJsonEncoder():

    def __init__(self, attendee):
        self._attendee = attendee

    def encode(self, format='string'):
        result = {}
        result['user_id'] = self._attendee.user_id
        result['present'] = self._attendee.present
        result['present_time'] = self._attendee.present_time

        if format == 'dict':
            return result
        return json.dumps(result)
