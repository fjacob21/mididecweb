from datetime import datetime, timedelta

ATTENDEE_LIST = 1
ALREADY_ATTENDEE_LIST = 2
WAITING_LIST = 3
ALREADY_WAITING_LIST = 4


class Event():

    def __init__(self, store, event_id):
        self._store = store
        self._event_id = event_id

    def get_data(self):
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

    # @property
    # def attendees(self):
    #     attendees = self.store.attendees.get_all(self._event_id)
    #     for
    #     return self._attendees
    #
    # @property
    # def waiting_attendees(self):
    #     return self._waitinglist
    #
    # def register_attendee(self, attendee):
    #     aidx = self.find_attendee(attendee.email)
    #     if aidx != -1:
    #         return ALREADY_ATTENDEE_LIST
    #     widx = self.find_waiting(attendee.email)
    #     if widx != -1:
    #         return ALREADY_WAITING_LIST
    #     if len(self._attendees) < self._max_attendee:
    #         self._attendees.append(attendee)
    #         return ATTENDEE_LIST
    #     self._waitinglist.append(attendee)
    #     return WAITING_LIST
    #
    # def cancel_registration(self, email):
    #     aidx = self.find_attendee(email)
    #     widx = self.find_waiting(email)
    #     if aidx == -1 and widx == -1:
    #         return None
    #     if aidx != -1:
    #         del self._attendees[aidx]
    #         if len(self._waitinglist):
    #             attendee = self._waitinglist[0]
    #             del self._waitinglist[0]
    #             self.register_attendee(attendee)
    #             return attendee
    #     else:
    #         del self._waitinglist[widx]
    #         return None
    #
    # def find_attendee(self, email):
    #     for i in range(len(self._attendees)):
    #         if self._attendees[i].email == email:
    #             return i
    #     return -1
    #
    # def find_waiting(self, email):
    #     for i in range(len(self._waitinglist)):
    #         if self._waitinglist[i].email == email:
    #             return i
    #     return -1
