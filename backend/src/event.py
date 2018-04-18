from datetime import datetime, timedelta
import hashlib
import pytz
import random

ATTENDEE_LIST = 1
ALREADY_ATTENDEE_LIST = 2
WAITING_LIST = 3
ALREADY_WAITING_LIST = 4


class Event():

    def __init__(self, title, desc, max_attendee=None,
                 start=None, duration=None,
                 location='', organizer_name='', organizer_email="", uid=''):
        if not start:
            start = datetime.now(pytz.timezone("America/New_York"))
        if not duration:
            duration = timedelta(hours=1)
        if not max_attendee:
            max_attendee = 20

        self._title = title
        self._description = desc
        self._max_attendee = max_attendee
        self._start = start
        self._duration = duration
        self._location = location
        self._organizer_name = organizer_name
        self._organizer_email = organizer_email
        if not uid:
            uid = self.generate_uid()
        self._uid = uid

        self._attendees = []
        self._waitinglist = []

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
    def max_attendee(self):
        return self._max_attendee

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

    @property
    def attendees(self):
        return self._attendees

    @property
    def waiting_attendees(self):
        return self._waitinglist

    def generate_uid(self):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((self.start + self.title + salt).encode())
        return hash.hexdigest()

    def register_attendee(self, attendee):
        aidx = self.find_attendee(attendee.email)
        if aidx != -1:
            return ALREADY_ATTENDEE_LIST
        widx = self.find_waiting(attendee.email)
        if widx != -1:
            return ALREADY_WAITING_LIST
        if len(self._attendees) < self._max_attendee:
            self._attendees.append(attendee)
            return ATTENDEE_LIST
        self._waitinglist.append(attendee)
        return WAITING_LIST

    def cancel_registration(self, email):
        aidx = self.find_attendee(email)
        widx = self.find_waiting(email)
        if aidx == -1 and widx == -1:
            return None
        if aidx != -1:
            del self._attendees[aidx]
            if len(self._waitinglist):
                attendee = self._waitinglist[0]
                del self._waitinglist[0]
                self.register_attendee(attendee)
                return attendee
        else:
            del self._waitinglist[widx]
            return None

    def find_attendee(self, email):
        for i in range(len(self._attendees)):
            if self._attendees[i].email == email:
                return i
        return -1

    def find_waiting(self, email):
        for i in range(len(self._waitinglist)):
            if self._waitinglist[i].email == email:
                return i
        return -1

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

        return result
