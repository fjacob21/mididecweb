from event import Event
from datetime import datetime, timedelta
import pytz
import hashlib
import random


class Events():

    def __init__(self, store):
        self._store = store

    def add(self, title, description, max_attendee=None, start=None,
            duration=None, location='', organizer_name='', organizer_email="",
            event_id='', owner=None, not_training=False):
        owner_id = ''
        if owner:
            owner_id = owner.user_id
        if not start:
            start = datetime.now(pytz.timezone("America/New_York"))
        if not duration:
            duration = timedelta(hours=1)
        if not max_attendee:
            max_attendee = 20
        if not event_id:
            event_id = self.generate_event_id(start, title)
        startstr = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_second = duration.total_seconds()
        self._store.events.create(title, description, max_attendee, startstr,
                                  duration_second, location, organizer_name,
                                  organizer_email, event_id, owner_id, not_training)
        return Event(self._store, event_id)

    def generate_event_id(self, start, title):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        startstr = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        hash.update((startstr + title + salt).encode())
        return hash.hexdigest()

    def remove(self, event_id):
        self._store.events.delete(event_id)
        self._store.attendees.delete_event(event_id)
        self._store.waitings.delete_event(event_id)
        self._store.attachments.delete_event(event_id)

    @property
    def list(self):
        result = []
        events = self._store.events.get_all()
        for event in events:
            result.append(Event(self._store, event['event_id']))
        return result

    @property
    def count(self):
        return len(self.list)

    def get(self, event_id):
        event = self._store.events.get(event_id)
        if event:
            return Event(self._store, event['event_id'])
        return None

    def find_owning_events(self, owner):
        events = []
        for event in self.list:
            if event.owner_id == owner.user_id:
                events.append(event)
        return events

    def is_user_attending_owning_events(self, owner, user):
        events = self.find_owning_events(owner)
        for event in events:
            if event.is_attending(user):
                return True
        return False
