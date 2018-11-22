from datetime import datetime, timedelta
import pytz

class MemoryAttendees():

    def __init__(self):
        self._attendees = []

    def add(self, user_id, event_id):
        attendee = {'user_id': user_id, 'event_id': event_id, 'present': False, 'present_time': ''}
        self._attendees.append(attendee)

    def get_all(self, event_id):
        attendees = []
        for attendee in self._attendees:
            if attendee['event_id'] == event_id:
                attendees.append(attendee)
        return attendees

    def get(self, user_id, event_id):
        idx = self.index(user_id, event_id)
        if idx == -1:
            return None
        return self._attendees[idx]

    def delete(self, user_id, event_id):
        idx = self.index(user_id, event_id)
        if idx != -1:
            del self._attendees[idx]

    def delete_event(self, event_id):
        newlist = []
        for attendee in self._attendees:
            if attendee['event_id'] != event_id:
                newlist.append(attendee)
        self._attendees = newlist

    def delete_user(self, user_id):
        newlist = []
        for attendee in self._attendees:
            if attendee['user_id'] != user_id:
                newlist.append(attendee)
        self._attendees = newlist

    def update(self, user_id, event_id, present):
        idx = self.index(user_id, event_id)
        if idx == -1:
            return False
        attendee = self._attendees[idx]
        if present:
            start = datetime.now(pytz.timezone("America/New_York"))
            startstr = start.strftime("%Y-%m-%dT%H:%M:%SZ")
            attendee['present_time'] = startstr
            attendee['present'] = True
        else:
            attendee['present_time'] = ''
            attendee['present'] = False
        return True

    def reset(self):
        self._attendees = []

    def clean(self):
        self.reset()

    def index(self, user_id, event_id):
        i = 0
        for attendee in self._attendees:
            if (attendee['event_id'] == event_id and
               attendee['user_id'] == user_id):
                return i
            i += 1
        return -1
