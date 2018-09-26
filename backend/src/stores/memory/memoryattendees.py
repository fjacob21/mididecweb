
class MemoryAttendees():

    def __init__(self):
        self._attendees = []

    def add(self, user_id, event_id):
        attendee = {'user_id': user_id, 'event_id': event_id}
        self._attendees.append(attendee)

    def get_alls(self):
        attendees = []
        for attendee in self._attendees:
            attendees.append(attendee)
        return attendees

    def get_all(self, event_id):
        attendees = []
        for attendee in self._attendees:
            if attendee['event_id'] == event_id:
                attendees.append(attendee)
        return attendees

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

    def reset(self):
        self._attendees = []

    def clean(self):
        self.reset()

    def backup(self):
        return ('attendees', self._attendees)

    def restore(self, backup):
        self._attendees = backup['attendees']

    def index(self, user_id, event_id):
        i = 0
        for attendee in self._attendees:
            if (attendee['event_id'] == event_id and
               attendee['user_id'] == user_id):
                return i
            i += 1
        return -1
