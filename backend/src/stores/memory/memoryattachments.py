
class MemoryAttachments():

    def __init__(self):
        self._attachments = []

    def add(self, path, event_id):
        attendee = {'path': path, 'event_id': event_id}
        self._attachments.append(attendee)

    def get_all(self, event_id):
        attendees = []
        for attendee in self._attachments:
            if attendee['event_id'] == event_id:
                attendees.append(attendee)
        return attendees

    def delete(self, path, event_id):
        idx = self.index(path, event_id)
        if idx != -1:
            del self._attachments[idx]

    def delete_event(self, event_id):
        newlist = []
        for attendee in self._attachments:
            if attendee['event_id'] != event_id:
                newlist.append(attendee)
        self._attachments = newlist

    def reset(self):
        self._attachments = []

    def clean(self):
        self.reset()

    def index(self, path, event_id):
        i = 0
        for attendee in self._attachments:
            if (attendee['event_id'] == event_id and
               attendee['path'] == path):
                return i
            i += 1
        return -1
