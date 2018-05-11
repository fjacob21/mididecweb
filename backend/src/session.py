from codec import EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder
from datetime import datetime, timedelta
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from icalgenerator import iCalGenerator
from bcrypt_hash import BcryptHash
from access import UserAddAccess, UserGetCompleteAccess, UserUpdateAccess
from access import UserRemoveAccess, EventGetCompleteAccess, EventAddAccess
from access import EventRemoveAccess, EventRegisterAccess, EventPublishAccess


class Session(object):

    def __init__(self, params, events, users, loginkey='', config=None):
        self._params = params
        self._loginkey = loginkey
        self._events = events
        self._users = users
        self._user = None
        self._config = config
        if loginkey:
            self._user = users.get(loginkey)
        if 'loginkey' in params:
            self._user = users.get(self._params["loginkey"])

    @property
    def user(self):
        return self._user

    @property
    def events(self):
        return self._events

    @property
    def users(self):
        return self._users

    def get_events(self):
        complete = EventGetCompleteAccess(self).granted()
        events_dict = EventsJsonEncoder(self._events, complete).encode('dict')
        return {'events': events_dict}

    def get_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        complete = EventGetCompleteAccess(self, event).granted()
        event_dict = EventJsonEncoder(event, complete).encode('dict')
        return {'event': event_dict}

    def get_event_ical(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        return iCalGenerator(event).generate()

    def add_event(self):
        if "title" not in self._params or "desc" not in self._params:
            print('missing tile or desc')
            return None

        if not EventAddAccess(self).granted():
            print('Access denied')
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
                             event_id, self._user)
        return {'event': EventJsonEncoder(e, True).encode('dict')}

    def remove_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not EventRemoveAccess(self, event).granted():
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
        if not EventRegisterAccess(self, event).granted():
            return None
        result = event.register_attendee(self.user)
        is_owner = event.owner_id == self.user.user_id
        complete = self.user.is_super_user or is_owner
        return {'result': result,
                'event': EventJsonEncoder(event, complete).encode('dict')}

    def unregister_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not self._params:
            return None
        if not self.user:
            return None
        promotee = event.cancel_registration(self.user)
        if not promotee:
            return None
        if promotee and promotee != self.user:
            pass  # send email to promotee
        is_owner = event.owner_id == self.user.user_id
        complete = self.user.is_super_user or is_owner
        return {'result': True,
                'event': EventJsonEncoder(event, complete).encode('dict')}

    def publish_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            return None
        if not EventPublishAccess(self, event).granted():
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
        complete = UserGetCompleteAccess(self).granted()
        users_dict = UsersJsonEncoder(self._users, complete).encode('dict')
        return {'users': users_dict}

    def get_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        complete = UserGetCompleteAccess(self, user).granted()
        user_dict = UserJsonEncoder(user, complete).encode('dict')
        return {'user': user_dict}

    def add_user(self):
        if not self._params:
            return None
        if ('email' not in self._params or
            'name' not in self._params or
            'alias' not in self._params or
           'password' not in self._params):
            return None

        if not UserAddAccess(self).granted():
            return None

        email = self._params["email"]
        name = self._params["name"]
        alias = self._params["alias"]
        password = self._params["password"]
        password = BcryptHash(password).encrypt()
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
        user = self._users.get(email)
        if user:
            return None
        user = self._users.get(alias)
        if user:
            return None
        user = self._users.add(email, name, alias, password, phone, useemail,
                               usesms, profile)
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def validate_user(self):
        if not self._params:
            return None

        email = ''
        if 'email' in self._params:
            email = self._params['email']
        alias = ''
        if 'alias' in self._params:
            alias = self._params['alias']

        emailok = not self._users.find_email(email)
        aliasok = not self._users.find_alias(alias)
        return {'emailok': emailok, 'aliasok': aliasok}

    def remove_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        if not UserRemoveAccess(self, user).granted():
            return None
        self._users.remove(user.user_id)
        return {'result': True}

    def update_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        if not UserUpdateAccess(self, user).granted():
            return None

        if 'email' in self._params:
            user.email = self._params['email']
        if 'name' in self._params:
            user.name = self._params['name']
        if 'alias' in self._params:
            user.alias = self._params['alias']
        if 'password' in self._params:
            password = BcryptHash(self._params['password']).encrypt()
            user.password = password
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
        password = BcryptHash(password, user.password.encode()).encrypt()
        loginkey = user.login(password)
        if not loginkey:
            return None
        user_dict = UserJsonEncoder(user, False, True).encode('dict')
        return {'user': user_dict}

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
