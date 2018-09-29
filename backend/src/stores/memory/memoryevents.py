from datetime import datetime
import pytz


class MemoryEvents():

    def __init__(self):
        self._events = []

    def create(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, event_id, owner_id, not_training=False):
        if not self.get(event_id):
            obj = self.create_object(title, description, max_attendee, start,
                                     duration, location, organizer_name,
                                     organizer_email, event_id, owner_id, not_training)
            self._events.append(obj)

    def get_all(self):
        return self._events

    def get(self, event_id):
        for event in self._events:
            if event['event_id'] == event_id:
                return event
        return None

    def update(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, not_training, event_id):
        event = self.get(event_id)
        if event:
            current = self._events[self.index(event_id)]
            obj = self.create_object(title, description, max_attendee, start,
                                     duration, location, organizer_name,
                                     organizer_email, event_id,
                                     current['owner_id'], not_training, current['create_date'])
            self._events[self.index(event_id)] = obj

    def delete(self, event_id):
        idx = self.index(event_id)
        if idx != -1:
            del self._events[idx]

    def reset(self):
        self._events = []

    def clean(self):
        self.reset()

    def create_object(self, title, description, max_attendee, start, duration,
                      location, organizer_name, organizer_email, event_id,
                      owner_id, not_training, create_date=''):
        if not create_date:
            create_date_dt = datetime.now(pytz.timezone("America/New_York"))
            create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        event = {}
        event['event_id'] = event_id
        event['title'] = title
        event['description'] = description
        event['max_attendee'] = max_attendee
        event['start'] = start
        event['duration'] = duration
        event['location'] = location
        event['organizer_name'] = organizer_name
        event['organizer_email'] = organizer_email
        event['owner_id'] = owner_id
        event['not_training'] = not_training
        event['create_date'] = create_date
        return event

    def index(self, event_id):
        i = 0
        for event in self._events:
            if event['event_id'] == event_id:
                return i
            i += 1
        return -1
