from datetime import datetime, timedelta
from user import User

ATTENDEE_LIST = 1
ALREADY_ATTENDEE_LIST = 2
WAITING_LIST = 3
ALREADY_WAITING_LIST = 4


class Event():

    def __init__(self, store, event_id):
        self._store = store
        self._event_id = event_id

    def get_data(self):
        print('event', self._event_id, self._store.events.get(self._event_id))
        return self._store.events.get(self._event_id)

    @property
    def event_id(self):
        return self._event_id

    @property
    def title(self):
        return self.get_data()['title']

    @property
    def description(self):
        return self.get_data()['description']

    @property
    def max_attendee(self):
        return int(self.get_data()['max_attendee'])

    @property
    def start(self):
        return self.get_data()['start']

    @property
    def duration(self):
        return int(self.get_data()['duration'])

    @property
    def end(self):
        start = datetime.strptime(self.start, "%Y-%m-%dT%H:%M:%SZ")
        dur = timedelta(seconds=self.duration)
        end = start + dur
        return end.strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def location(self):
        return self.get_data()['location']

    @property
    def organizer_name(self):
        return self.get_data()['organizer_name']

    @property
    def organizer_email(self):
        return self.get_data()['organizer_email']

    def __eq__(self, value):
        return self.get_data() == value.get_data()

    @property
    def attendees(self):
        result = []
        attendees = self._store.attendees.get_all(self._event_id)
        for attendee in attendees:
            result.append(User(self._store, attendee['user_id']))
        return result

    @property
    def waiting_attendees(self):
        result = []
        waitings = self._store.waitings.get_all(self._event_id)
        for attendee in waitings:
            result.append(User(self._store, attendee['user_id']))
        return result

    def register_attendee(self, user):
        aidx = self.find_attendee(user.email)
        if aidx != -1:
            return ALREADY_ATTENDEE_LIST
        widx = self.find_waiting(user.email)
        if widx != -1:
            return ALREADY_WAITING_LIST
        if len(self.attendees) < self.max_attendee:
            self._store.attendees.add(user.user_id, self.event_id)
            return ATTENDEE_LIST
        self._store.waitings.add(user.user_id, self.event_id)
        return WAITING_LIST

    def cancel_registration(self, email):
        aidx = self.find_attendee(email)
        widx = self.find_waiting(email)
        if aidx == -1 and widx == -1:
            return None
        if aidx != -1:
            self._store.attendees.delete(self.attendees[aidx].user_id, self._event_id)
            if len(self.waiting_attendees):
                attendee = self.waiting_attendees[0]
                self._store.waitings.delete(self.waiting_attendees[0].user_id, self._event_id)
                self.register_attendee(attendee)
                return attendee
        else:
            self._store.waitings.delete(self.waiting_attendees[widx].user_id, self._event_id)
            return None

    def find_attendee(self, email):
        for i in range(len(self.attendees)):
            if self.attendees[i].email == email:
                return i
        return -1

    def find_waiting(self, email):
        for i in range(len(self.waiting_attendees)):
            if self.waiting_attendees[i].email == email:
                return i
        return -1
