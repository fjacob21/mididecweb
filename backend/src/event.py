from datetime import datetime, timedelta
import json
import hashlib
import pytz
import random


class Event():

    def __init__(self, title, desc,
                 start=None, duration=None,
                 location='', organizer_name='', organizer_email="", uid=''):
        if not start:
            start = datetime.now(pytz.timezone("America/New_York"))
        if not duration:
            duration = timedelta(hours=1)

        self._title = title
        self._description = desc
        self._start = start
        self._duration = duration
        self._location = location
        self._organizer_name = organizer_name
        self._organizer_email = organizer_email
        if not uid:
            uid = self.generate_uid()
        self._uid = uid

    @property
    def uid(self):
        return self._uid

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def start(self):
        return self._start.strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def duration(self):
        return self._duration.total_seconds()

    @property
    def end(self):
        end = self._start + self._duration
        return end.strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def location(self):
        return self._location

    @property
    def organizer_name(self):
        return self._organizer_name

    @property
    def organizer_email(self):
        return self._organizer_email

    def generate_uid(self):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((self.start + self.title + salt).encode())
        return hash.hexdigest()

    @property
    def json(self):
        result = {}
        result['uid'] = self.uid
        result['title'] = self.title
        result['description'] = self.description
        result['start'] = self.start
        result['duration'] = self.duration
        result['end'] = self.end
        result['location'] = self.location
        result['organizer_name'] = self.organizer_name
        result['organizer_email'] = self.organizer_email

        return json.dumps(result)
