from codec import AttendeeJsonEncoder, EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder


class Session(object):

    def __init__(self, params, events, users, loginkey=''):
        self._params = params
        self._loginkey = loginkey
        self._events = events
        self._users = users
        self._user = users.get(loginkey)

    def get_events(self):
        events_dict = EventsJsonEncoder(self._events).encode('dict')
        return {'events': events_dict}

    def get_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return {'error': 'invalid event'}
        event_dict = EventJsonEncoder(event).encode('dict')
        return {'event': event_dict}

    def get_event_ical(self, event_id):
        pass

    def add_event(self):
        pass

    def remove_event(self, event_id):
        pass

    def update_event(self, event_id):
        pass

    def register_event(self, event_id):
        pass

    def unregister_event(self, event_id):
        pass

    def publish_event(self, event_id):
        pass

    def get_users(self):
        pass

    def get_user(self, user_id):
        pass

    def add_user(self):
        pass

    def remove_user(self, user_id):
        pass

    def update_user(self, user_id):
        pass

    def login(self, user_id):
        pass

    def logout(self, user_id):
        pass
