import json
import os
from .user_json_encoder import UserJsonEncoder
from .attendee_json_encoder import AttendeeJsonEncoder


class EventJsonEncoder():

    def __init__(self, event, complete=False, show_attendee=True, show_attachments=True):
        self._event = event
        self._complete = complete
        self._show_attendee = show_attendee
        self._show_attachments = show_attachments

    def encode(self, format='string'):
        result = {}
        result['event_id'] = self._event.event_id
        result['title'] = self._event.title
        result['max_attendee'] = self._event.max_attendee
        result['description'] = self._event.description
        result['start'] = self._event.start
        result['duration'] = self._event.duration
        result['end'] = self._event.end
        result['location'] = self._event.location
        result['organizer_name'] = self._event.organizer_name
        result['owner_id'] = self._event.owner_id
        result['create_date'] = self._event.create_date
        result['not_training'] = self._event.not_training
        print('event codec', self._event.not_training)
        if self._complete:
            result['organizer_email'] = self._event.organizer_email
        if self._show_attendee:
            attendees = []
            for a in self._event.attendees:
                attendees.append(AttendeeJsonEncoder(a).encode('dict'))
            result['attendees'] = attendees
            waitings = []
            for a in self._event.waiting_attendees:
                waitings.append(UserJsonEncoder(a, self._complete).encode('dict'))
            result['waitings'] = waitings
        if self._show_attachments:
            attachments = []
            for a in self._event.attachments:
                name = os.path.basename(a)
                attachments.append(name)
            result['attachments'] = attachments

        if format == 'dict':
            return result
        return json.dumps(result)
