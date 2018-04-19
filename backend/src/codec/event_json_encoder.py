import json
from .user_json_encoder import UserJsonEncoder


class EventJsonEncoder():

    def __init__(self, event, complete=False, show_attendee=True):
        self._event = event
        self._complete = complete
        self._show_attendee = show_attendee

    def encode(self, format='string'):
        result = {}
        result['uid'] = self._event.uid
        result['title'] = self._event.title
        result['max_attendee'] = self._event.max_attendee
        result['description'] = self._event.description
        result['start'] = self._event.start
        result['duration'] = self._event.duration
        result['end'] = self._event.end
        result['location'] = self._event.location
        result['organizer_name'] = self._event.organizer_name
        if self._complete:
            result['organizer_email'] = self._event.organizer_email
        if self._show_attendee:
            attendees = []
            for a in self._event.attendees:
                attendees.append(UserJsonEncoder(a, self._complete).encode('dict'))
            result['attendees'] = attendees
            waitings = []
            for a in self._event.waiting_attendees:
                waitings.append(UserJsonEncoder(a, self._complete).encode('dict'))
            result['waitings'] = waitings

        if format == 'dict':
            return result
        return json.dumps(result)
