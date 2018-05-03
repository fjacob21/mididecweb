from codec import EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder
from datetime import datetime, timedelta
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from icalgenerator import iCalGenerator


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
            return None
        event_dict = EventJsonEncoder(event).encode('dict')
        return {'event': event_dict}

    def get_event_ical(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        return iCalGenerator(event).generate()

    def add_event(self):
        if "title" not in self._params or "desc" not in self._params:
            return None

        title = self._params["title"]
        desc = self._params["desc"]
        max_attendee = None
        if "max_attendee" in self._params:
            max_attendee = self._params["max_attendee"]
        start = None
        if "start" in self._params:
            start = self._params["start"]
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        duration = None
        if "duration" in self._params:
            duration = int(self._params["duration"])
            duration = timedelta(seconds=duration)
        location = ''
        if "location" in self._params:
            location = self._params["location"]
        organizer_name = ''
        if "organizer_name" in self._params:
            organizer_name = self._params["organizer_name"]
        organizer_email = ''
        if "organizer_email" in self._params:
            organizer_email = self._params["organizer_email"]
        event_id = ''
        if "event_id" in self._params:
            event_id = self._params["event_id"]
        e = self._events.add(title, desc, max_attendee, start, duration,
                             location, organizer_name, organizer_email,
                             event_id)
        return {'event': EventJsonEncoder(e).encode('dict')}

    def remove_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        self._events.remove(event_id)
        return {'result': True}

    def update_event(self, event_id):
        pass

    def register_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not self._params:
            return None
        if "name" not in self._params or "email" not in self._params:
            return None

        name = self._params["name"]
        email = self._params["email"]
        phone = ''
        if "phone" in self._params:
            phone = self._params["phone"]
        useemail = False
        if "useemail" in self._params:
            useemail = self._params["useemail"]
        usesms = False
        if "usesms" in self._params:
            usesms = self._params["usesms"]
        user = self._users.add(email, name, name, '', phone, useemail, usesms)
        result = event.register_attendee(user)
        return {'result': result}

    def unregister_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not self._params:
            return None
        if "email" not in self._params:
            return None
        email = self._params["email"]
        if event.find_attendee(email) == -1 and event.find_waiting(email) == -1:
            return None
        promotee = event.cancel_registration(email)
        if promotee:
            pass  # send email to promotee
        return {'result': True}

    def publish_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not self._params:
            return None
        if ("usr" not in self._params or "psw" not in self._params or
           'sid' not in self._params or 'token' not in self._params):
            return None
        usr = self._params["usr"]
        psw = self._params["psw"]
        sid = self._params["sid"]
        token = self._params["token"]
        body = EventTextGenerator(event, False).generate()
        res = True
        for user in self._users.list:
            if user.useemail and user.email:
                sender = EmailSender(usr, psw,
                                     user.email, event.title, body)
                res = sender.send()
            if user.usesms and user.phone:
                sender = SmsSender(sid, token,
                                   user.phone, event.title, body)
                res = sender.send()
        if not res:
            return None
        return {'result': True}

    def get_users(self):
        users_dict = UsersJsonEncoder(self._users).encode('dict')
        return {'users': users_dict}

    def get_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def add_user(self):
        if not self._params:
            return None
        if ('email' not in self._params or
            'name' not in self._params or
            'alias' not in self._params or
           'password' not in self._params):
            return None
        email = self._params["email"]
        name = self._params["name"]
        alias = self._params["alias"]
        password = self._params["password"]
        phone = ''
        if 'phone' in self._params:
            phone = self._params['phone']
        useemail = True
        if 'useemail' in self._params:
            useemail = self._params['useemail']
        usesms = False
        if 'usesms' in self._params:
            usesms = self._params['usesms']
        profile = ''
        if 'profile' in self._params:
            profile = self._params['profile']
        user = self._users.add(email, name, alias, password, phone, useemail,
                               usesms, profile)
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def remove_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        self._users.remove(user.user_id)
        return {'result': True}

    def update_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None

        if 'email' in self._params:
            user.email = self._params['email']
        if 'name' in self._params:
            user.name = self._params['name']
        if 'alias' in self._params:
            user.alias = self._params['alias']
        if 'password' in self._params:
            user.password = self._params['password']
        if 'phone' in self._params:
            user.phone = self._params['phone']
        if 'useemail' in self._params:
            user.useemail = self._params['useemail']
        if 'usesms' in self._params:
            user.usesms = self._params['usesms']
        if 'profile' in self._params:
            user.profile = self._params['profile']
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def login(self, user_id):
        if not self._params:
            return None
        if "password" not in self._params:
            return None
        password = self._params["password"]
        user = self._users.get(user_id)
        if not user:
            return None
        loginkey = user.login(password)
        if not loginkey:
            return None
        return {'loginkey': loginkey}

    def logout(self, user_id):
        if not self._params:
            return None
        if "loginkey" not in self._params:
            return None
        loginkey = self._params["loginkey"]
        user = self._users.get(user_id)
        if not user:
            return None
        if not user.logout(loginkey):
            return None
        return {'result': True}
