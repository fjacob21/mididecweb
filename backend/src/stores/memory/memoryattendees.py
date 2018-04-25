
class MemoryAttendees():

    def __init__(self):
        self._attendees = []

    def add(self, user_id, event_id):
        attendee = {'user_id': user_id, 'event_id': event_id}
        self._attendees.append(attendee)

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
