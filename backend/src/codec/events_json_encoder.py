import json
from .event_json_encoder import EventJsonEncoder


class EventsJsonEncoder():

    def __init__(self, events, complete=False, show_attendee=True):
        self._events = events
        self._complete = complete
        self._show_attendee = show_attendee

    def encode(self, format='string'):
        result = {}
        result['count'] = self._events.count
        events = []
        for ev in self._events.list:
            events.append(EventJsonEncoder(ev, self._complete).encode('dict'))
        result['events'] = events
        if format == 'dict':
            return result
        return json.dumps(result)
