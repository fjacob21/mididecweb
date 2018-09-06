from datetime import datetime, timedelta
from user import User
from session_exception import SessionError
import errors

ATTENDEE_LIST = 1
ALREADY_ATTENDEE_LIST = 2
WAITING_LIST = 3
ALREADY_WAITING_LIST = 4


class Event():

    def __init__(self, store, event_id, static_data=None):
        self._store = store
        self._event_id = event_id
        self._static_data = static_data

    def get_data(self):
        if self._static_data:
            return self._static_data
        return self._store.events.get(self._event_id)

    def update_data(self, data):
        if self._static_data:
            self._static_data = data
        else:
            self._store.events.update(data['title'],
                                      data['description'], data['max_attendee'],
                                      data['start'], data['duration'],
                                      data['location'], data['organizer_name'],
                                      data['organizer_email'], self._event_id)

    @property
    def owner_id(self):
        return self.get_data()['owner_id']

    @property
    def event_id(self):
        return self._event_id

    @property
    def title(self):
        return self.get_data()['title']

    @title.setter
    def title(self, value):
        data = self.get_data()
        data['title'] = value
        self.update_data(data)

    @property
    def description(self):
        return self.get_data()['description']

    @description.setter
    def description(self, value):
        data = self.get_data()
        data['description'] = value
        self.update_data(data)

    @property
    def max_attendee(self):
        return int(self.get_data()['max_attendee'])

    @max_attendee.setter
    def max_attendee(self, value):
        data = self.get_data()
        data['max_attendee'] = value
        self.update_data(data)

    @property
    def start(self):
        return self.get_data()['start']

    @start.setter
    def start(self, value):
        data = self.get_data()
        data['start'] = value
        self.update_data(data)

    @property
    def duration(self):
        return int(self.get_data()['duration'])

    @duration.setter
    def duration(self, value):
        data = self.get_data()
        data['duration'] = value
        self.update_data(data)

    @property
    def end(self):
        start = datetime.strptime(self.start, "%Y-%m-%dT%H:%M:%SZ")
        dur = timedelta(seconds=self.duration)
        end = start + dur
        return end.strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def location(self):
        return self.get_data()['location']

    @location.setter
    def location(self, value):
        data = self.get_data()
        data['location'] = value
        self.update_data(data)

    @property
    def organizer_name(self):
        return self.get_data()['organizer_name']

    @organizer_name.setter
    def organizer_name(self, value):
        data = self.get_data()
        data['organizer_name'] = value
        self.update_data(data)

    @property
    def organizer_email(self):
        return self.get_data()['organizer_email']

    @organizer_email.setter
    def organizer_email(self, value):
        data = self.get_data()
        data['organizer_email'] = value
        self.update_data(data)

    def __eq__(self, value):
        return self.get_data() == value.get_data()

    @property
    def create_date(self):
        return self.get_data()['create_date']

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

    @property
    def all_attendees(self):
        return self.attendees + self.waiting_attendees

    def register_attendee(self, user):
        aidx = self.find_attendee(user)
        if aidx != -1:
            return ALREADY_ATTENDEE_LIST
        widx = self.find_waiting(user)
        if widx != -1:
            return ALREADY_WAITING_LIST
        if len(self.attendees) < self.max_attendee:
            self._store.attendees.add(user.user_id, self.event_id)
            return ATTENDEE_LIST
        self._store.waitings.add(user.user_id, self.event_id)
        return WAITING_LIST

    def cancel_registration(self, user):
        aidx = self.find_attendee(user)
        widx = self.find_waiting(user)
        if aidx == -1 and widx == -1:
            raise SessionError(errors.ERROR_NOT_REGISTERED)
        if aidx != -1:
            self._store.attendees.delete(self.attendees[aidx].user_id, self._event_id)
            if len(self.waiting_attendees):
                attendee = self.waiting_attendees[0]
                self._promote_waiting(attendee)
                return attendee
            return user
        else:
            self._store.waitings.delete(self.waiting_attendees[widx].user_id, self._event_id)
            return user

    def promote_waitings(self, number):
        promotees = self.waiting_attendees
        if len(self.waiting_attendees) >= number:
            promotees = self.waiting_attendees[:number]
        for promotee in promotees:
            self._promote_waiting(promotee)
        return promotees

    def _promote_waiting(self, waiting):
        self._store.waitings.delete(waiting.user_id, self._event_id)
        self.register_attendee(waiting)

    def find_attendee(self, user):
        for i in range(len(self.attendees)):
            if self.attendees[i].user_id == user.user_id:
                return i
        return -1

    def find_waiting(self, user):
        for i in range(len(self.waiting_attendees)):
            if self.waiting_attendees[i].user_id == user.user_id:
                return i
        return -1

    def is_attending(self, user):
        attendees = self.all_attendees
        for attendee in attendees:
            if attendee.user_id == user.user_id:
                return True
        return False

    @property
    def attachments(self):
        result = []
        attachments = self._store.attachments.get_all(self._event_id)
        for attachment in attachments:
            result.append(attachment['path'])
        return result
    
    def add_attachment(self, path):
        aidx = self.find_attachment(path)
        if aidx != -1:
            raise SessionError(errors.ERROR_ATTACHMENT_PRESENT)
        self._store.attachments.add(path, self.event_id)
    
    def remove_attachment(self, path):
        aidx = self.find_attachment(path)
        if aidx == -1:
            raise SessionError(errors.ERROR_INVALID_ATTACHMENT)
        self._store.attachments.delete(self.attachments[aidx], self._event_id)

    def find_attachment(self, path):
        for i in range(len(self.attachments)):
            if self.attachments[i] == path:
                return i
        return -1