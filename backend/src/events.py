

class Events():

    def __init__(self):
        self._events = []

    def add(self, event):
        self._events.append(event)

    def remove(self, uid):
        idx = self.index(uid)
        if idx != -1:
            del self._events[idx]

    @property
    def list(self):
        return self._events

    @property
    def count(self):
        return len(self._events)

    def get(self, uid):
        for event in self._events:
            if event.uid == uid:
                return event
        return None

    def index(self, uid):
        for i in range(self.count):
            if self._events[i].uid == uid:
                return i
        return -1
