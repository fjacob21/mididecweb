
class MemoryWaitings():

    def __init__(self):
        self._waitings = []

    def add(self, user_id, event_id):
        waiting = {'user_id': user_id, 'event_id': event_id}
        self._waitings.append(waiting)

    def get_all(self, event_id):
        waitings = []
        for waiting in self._waitings:
            if waiting['event_id'] == event_id:
                waitings.append(waiting)
        return waitings

    def delete(self, user_id, event_id):
        idx = self.index(user_id, event_id)
        if idx != -1:
            del self._waitings[idx]

    def delete_event(self, event_id):
        newlist = []
        for attendee in self._waitings:
            if attendee['event_id'] != event_id:
                newlist.append(attendee)
        self._waitings = newlist

    def delete_user(self, user_id):
        newlist = []
        for attendee in self._waitings:
            if attendee['user_id'] != user_id:
                newlist.append(attendee)
        self._waitings = newlist

    def reset(self):
        self._waitings = []

    def clean(self):
        self.reset()

    def index(self, user_id, event_id):
        i = 0
        for waiting in self._waitings:
            if (waiting['event_id'] == event_id and
               waiting['user_id'] == user_id):
                return i
            i += 1
        return -1
