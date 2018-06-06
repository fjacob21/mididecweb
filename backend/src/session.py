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
from access import EventUpdateAccess
from event import ATTENDEE_LIST, WAITING_LIST
from jinja2 import Environment, FileSystemLoader
from session_exception import SessionError
import errors
import locale
import os
from events import Events
from users import Users


class Session(object):

    def __init__(self, params, store, loginkey='', config=None,
                 server='https://mididecouverte.org/'):
        self._params = params
        self._loginkey = loginkey
        self._events = Events(store)
        self._users = Users(store)
        self._user = None
        self._config = config
        self._server = server
        if loginkey:
            self._user = self._users.get(loginkey)
        if 'loginkey' in params and self._params["loginkey"]:
            self._user = self._users.get(self._params["loginkey"])

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
            raise SessionError(errors.ERROR_INVALID_EVENT)
        complete = EventGetCompleteAccess(self, event).granted()
        event_dict = EventJsonEncoder(event, complete).encode('dict')
        return {'event': event_dict}

    def get_event_ical(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        return iCalGenerator(event).generate()

    def get_event_jinja(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        env = Environment(loader=FileSystemLoader('emails'))
        t = env.get_template('promotee.html')

        event_obj = self.generate_email_event(event)
        html = t.render(user=self.user, event=event_obj, server=self._server)
        sender = EmailSender(self._config.email_user,
                             self._config.email_password,
                             'fjacob21@hotmail.com',
                             'Confirmation MidiDecouverte',
                             html,
                             'html',
                             self._config.email_server)
        sender.send()
        return html

    def add_event(self):
        if "title" not in self._params or "description" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)

        if not EventAddAccess(self).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)

        title = self._params["title"]
        description = self._params["description"]
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
        e = self._events.add(title, description, max_attendee, start, duration,
                             location, organizer_name, organizer_email,
                             event_id, self._user)
        print(max_attendee, duration, description)
        return {'event': EventJsonEncoder(e, True).encode('dict')}

    def remove_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventRemoveAccess(self, event).granted():
            print('Access denied')
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        self._events.remove(event_id)
        return {'result': True}

    def update_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventUpdateAccess(self, event).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)

        if 'title' in self._params:
            event.title = self._params['title']
        if 'description' in self._params:
            event.description = self._params['description']
        if 'max_attendee' in self._params:
            event.max_attendee = self._params['max_attendee']
        if 'start' in self._params:
            start = self._params["start"]
            event.start = start
        if 'duration' in self._params:
            duration = int(self._params["duration"])
            event.duration = duration
        if 'location' in self._params:
            event.location = self._params['location']
        return {'event': EventJsonEncoder(event, True).encode('dict')}

    def register_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not EventRegisterAccess(self, event).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        result = event.register_attendee(self.user)
        if result == ATTENDEE_LIST or result == WAITING_LIST:
            self.send_confirmation_email(result, event, self.user)
        is_owner = event.owner_id == self.user.user_id
        complete = self.user.is_super_user or is_owner
        return {'result': result,
                'event': EventJsonEncoder(event, complete).encode('dict')}

    def send_confirmation_email(self, list, event, user):
        if (self._config and self._config.email_user and
           self._config.email_password and self._config.email_server):
            env = Environment(loader=FileSystemLoader('emails'))
            event_obj = self.generate_email_event(event)
            if list == ATTENDEE_LIST:
                t = env.get_template('registerconfirm.html')
            else:
                t = env.get_template('waitingconfirm.html')
            sender = EmailSender(self._config.email_user,
                                 self._config.email_password,
                                 user.email,
                                 'Confirmation pour ' + event.title,
                                 t.render(user=user,
                                          event=event_obj,
                                          server=self._server),
                                 'html',
                                 self._config.email_server)
            sender.send()

    def unregister_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not self.user:
            raise SessionError(errors.ERROR_LOGIN_NEEDED)
        promotee = event.cancel_registration(self.user)
        if promotee and promotee != self.user:
            self.send_promotee_email(event, promotee)
        is_owner = event.owner_id == self.user.user_id
        complete = self.user.is_super_user or is_owner
        return {'result': True,
                'event': EventJsonEncoder(event, complete).encode('dict')}

    def send_promotee_email(self, event, promotee):
        if (self._config and self._config.email_user and
           self._config.email_password and self._config.email_server):
            event_obj = self.generate_email_event(event)
            env = Environment(loader=FileSystemLoader('emails'))
            t = env.get_template('promotee.html')
            sender = EmailSender(self._config.email_user,
                                 self._config.email_password,
                                 promotee.email,
                                 'Confirmation pour' + event.title,
                                 t.render(user=promotee,
                                          event=event_obj,
                                          server=self._server),
                                 'html',
                                 self._config.email_server)
            sender.send()

    def publish_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventPublishAccess(self, event).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        self.send_publish_event_email(event)
        self.send_publish_event_sms(event)
        return {'result': True}

    def send_publish_event_email(self, event):
        if (self._config and self._config.email_user and
           self._config.email_password and self._config.email_server):
            env = Environment(loader=FileSystemLoader('emails'))
            t = env.get_template('eventpublish.html')
            event_obj = self.generate_email_event(event)
            res = True
            for user in self._users.list:
                if user.useemail and user.email and user.validated:
                    sender = EmailSender(self._config.email_user,
                                         self._config.email_password,
                                         user.email,
                                         'Nouvelle rencontre',
                                         t.render(user=user,
                                                  event=event_obj,
                                                  server=self._server),
                                         'html',
                                         self._config.email_server)
                    res = sender.send()
            if not res:
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def send_publish_event_sms(self, event):
        if self._config and self._config.sms_sid and self._config.sms_token:
            body = EventTextGenerator(event, False).generate()
            res = True
            for user in self._users.list:
                if (user.usesms and user.phone and user.validated and
                   user.smsvalidated):
                    sender = SmsSender(self._config.sms_sid,
                                       self._config.sms_token, user.phone,
                                       event.title, body)
                    res = sender.send()
            if not res:
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def get_users(self):
        complete = UserGetCompleteAccess(self).granted()
        users_dict = UsersJsonEncoder(self._users, complete).encode('dict')
        return {'users': users_dict}

    def get_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        complete = UserGetCompleteAccess(self, user).granted()
        user_dict = UserJsonEncoder(user, complete).encode('dict')
        return {'user': user_dict}

    def get_user_avatar(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not user.avatar_path:
            raise SessionError(errors.ERROR_NO_AVATAR)
        return user.avatar_path

    def add_user(self):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if ('email' not in self._params or
            'name' not in self._params or
            'alias' not in self._params or
           'password' not in self._params):
            raise SessionError(errors.ERROR_MISSING_PARAMS)

        if not UserAddAccess(self).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)

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
            raise SessionError(errors.ERROR_INVALID_USER)
        user = self._users.get(alias)
        if user:
            raise SessionError(errors.ERROR_INVALID_USER)
        user = self._users.add(email, name, alias, password, phone, useemail,
                               usesms, profile)
        self.send_validation_email(user)
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def send_validation_email(self, user):
        if (self._config and self._config.email_user and
           self._config.email_password and self._config.email_server):
            env = Environment(loader=FileSystemLoader('emails'))
            t = env.get_template('uservalidate.html')
            sender = EmailSender(self._config.email_user,
                                 self._config.email_password,
                                 user.email,
                                 'Validation MidiDecouverte',
                                 t.render(user=user,
                                          server=self._server),
                                 'html',
                                 self._config.email_server)
            sender.send()
        else:
            user.validated = True

    def validate_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        user.validated = True
        env = Environment(loader=FileSystemLoader('emails'))
        t = env.get_template('uservalidated.html')
        return t.render(user=user, server=self._server)

    def sendcode(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserAddAccess(self).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        code = user.generate_sms_code()
        self.send_sms_code(user, code)
        return {'result': True}

    def send_sms_code(self, user, code):
        if self._config and self._config.sms_sid and self._config.sms_token:
            res = False
            if user.phone and user.validated:
                    sender = SmsSender(self._config.sms_sid,
                                       self._config.sms_token, user.phone,
                                       'validation code', code)
                    res = sender.send()
            if not res:
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def validatecode(self, user_id):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserAddAccess(self).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if 'smscode' not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        smscode = self._params["smscode"]
        return {'result': user.validate_sms_code(smscode)}

    def validate_user_info(self):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)

        user_id = ''
        if 'user_id' in self._params:
            user_id = self._params['user_id']
        user = self._users.get(user_id)
        email = ''
        if 'email' in self._params:
            email = self._params['email']
        alias = ''
        if 'alias' in self._params:
            alias = self._params['alias']
        sameemail = False
        if self.user and email == self.user.email or user and user.email == email:
            sameemail = True
        samealias = False
        if self.user and alias == self.user.alias or user and user.alias == alias:
            samealias = True

        emailok = not self._users.find_email(email) or sameemail
        aliasok = not self._users.find_alias(alias) or samealias
        return {'emailok': emailok, 'aliasok': aliasok}

    def remove_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserRemoveAccess(self, user).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if user.avatar_path:
            os.remove(user.avatar_path)
        self._users.remove(user.user_id)
        return {'result': True}

    def update_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserUpdateAccess(self, user).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)

        if 'email' in self._params:
            user.email = self._params['email']
        if 'name' in self._params:
            user.name = self._params['name']
        if 'alias' in self._params:
            user.alias = self._params['alias']
        if 'password' in self._params:
            if self._params['password']:
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
        if self.user.is_super_user and 'access' in self._params:
            user.access = self._params['access']
        user_dict = UserJsonEncoder(user).encode('dict')
        return {'user': user_dict}

    def update_user_avatar(self, user_id, avatar):
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserUpdateAccess(self, user).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        avatar_path = '../data/img/users/' + user.user_id + '.jpg'
        user.avatar_path = avatar_path
        avatar.save(avatar_path)
        return {'result': True}

    def login(self, user_id):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "password" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        password = self._params["password"]
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_LOGIN)
        password = BcryptHash(password, user.password.encode()).encrypt()
        user.login(password)
        user_dict = UserJsonEncoder(user, False, True).encode('dict')
        return {'user': user_dict}

    def logout(self, user_id):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "loginkey" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        loginkey = self._params["loginkey"]
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not user.logout(loginkey):
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        return {'result': True}

    def generate_email_event(self, event):
        event_obj = {}
        event_obj['event_id'] = event.event_id
        event_obj['title'] = event.title
        try:
            locale.setlocale(locale.LC_ALL, 'fr_CA')
        except Exception:
            pass
        start = datetime.strptime(event.start, "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(event.end, "%Y-%m-%dT%H:%M:%SZ")
        event_obj['day'] = start.strftime("%A")
        event_obj['start'] = start.strftime("%d %B %Y")
        event_obj['times'] = start.strftime("%H:%M %Z") + ' - ' + end.strftime("%H:%M %Z")
        event_obj['description'] = event.description
        event_obj['location'] = event.location
        event_obj['organizer_name'] = event.organizer_name
        return event_obj
