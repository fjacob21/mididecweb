from codec import EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder
from datetime import datetime, timedelta
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from email_generators import iCalGenerator
from bcrypt_hash import BcryptHash
from access import UserAddAccess, UserGetCompleteAccess, UserUpdateAccess
from access import UserRemoveAccess, EventGetCompleteAccess, EventAddAccess
from access import EventRemoveAccess, EventRegisterAccess, EventPublishAccess
from access import EventUpdateAccess, UserResetPasswordAccess
from event import ATTENDEE_LIST, WAITING_LIST
from jinja2 import Environment, FileSystemLoader
from session_exception import SessionError
import errors
import locale
import os
from events import Events
from event import Event
from users import Users
from passwordresetrequests import PasswordResetRequests
from email_generators import generate_email
from email_generators import UserValidationEmail, EventPublishEmail
from email_generators import UserPromoteEmail, UserEventConfirmEmail
from email_generators import EventDateChangedEmail, EventLocationChangedEmail
from email_generators import UserEventWaitEmail, UserResetPasswordEmail

class Session(object):

    def __init__(self, params, store, loginkey='', config=None,
                 server='https://mididecouverte.org/'):
        self._params = params
        self._store = store
        self._loginkey = loginkey
        self._events = Events(store)
        self._users = Users(store)
        self._reset_password_requests = PasswordResetRequests(store)
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

        old_event = event.get_data()
        old_event = Event(self._store, event_id, static_data=old_event)
        old_event.start = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        email = EventPublishEmail(event=event, server=self._server)
        email = UserValidationEmail(server=self._server)
        email = UserPromoteEmail(event=event, server=self._server)
        email = UserEventConfirmEmail(event=event, server=self._server)
        email = UserEventWaitEmail(event=event, server=self._server)
        email = UserResetPasswordEmail(request_id='2609fcd001a971a0436e633ed04336b35ac3974d9bcf098afbe1172b1799d458', server=self._server)
        #html = generate_email('test', 'usertest.html')#, root='../src')
        #email = EventDateChangedEmail(event=event, old_event=old_event, server=self._server)
        #email = EventLocationChangedEmail(event=event, old_event=old_event, server=self._server)
        self.send_email(email, [self.user])
        return email.generate(user=self.user)

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
        return {'event': EventJsonEncoder(e, True).encode('dict')}

    def remove_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventRemoveAccess(self, event).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        self._events.remove(event_id)
        return {'result': True}

    def update_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventUpdateAccess(self, event).granted():
            raise SessionError(errors.ERROR_ACCESS_DENIED)

        old_event = event.get_data()
        old_event = Event(self._store, event_id, static_data=old_event)
        date_changed = False
        location_changed = False
        if 'title' in self._params:
            event.title = self._params['title']
        if 'description' in self._params:
            event.description = self._params['description']
        if 'max_attendee' in self._params:
            event.max_attendee = self._params['max_attendee']
        if 'start' in self._params:
            start = self._params["start"]
            if start != event.start:
                event.start = start
                date_changed = True
        if 'duration' in self._params:
            duration = int(self._params["duration"])
            if duration != event.duration:
                event.duration = duration
                date_changed = True
        if 'location' in self._params:
            location = self._params['location']
            if location != event.location:
                event.location = location
                location_changed = True
        if location_changed:
            self.send_location_changed_email(event, old_event)
        if date_changed:
            self.send_date_changed_email(event, old_event)
        return {'event': EventJsonEncoder(event, True).encode('dict')}

    def send_location_changed_email(self, event, old_event):
        email = EventLocationChangedEmail(event=event, old_event=old_event, server=self._server)
        self.send_email(email, event.attendees)

    def send_date_changed_email(self, event, old_event):
        email = EventDateChangedEmail(event=event, old_event=old_event, server=self._server)
        self.send_email(email, event.attendees)

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
        if list == ATTENDEE_LIST:
            email = UserEventConfirmEmail(event=event, server=self._server)
        else:
            email = UserEventWaitEmail(event=event, server=self._server)
        self.send_email(email, [user])


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
        email = UserPromoteEmail(event=event, server=self._server)
        self.send_email(email, [promotee])

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
        email = EventPublishEmail(event=event, server=self._server)
        self.send_email(email, self._users.list)

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
            email = UserValidationEmail(server=self._server)
            self.send_email(email, [user])
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
        if (self.user and email == self.user.email or user and user.email == email):
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

    def login(self, user_id, ip=''):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "password" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        password = self._params["password"]
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_LOGIN)
        password = BcryptHash(password, user.password.encode()).encrypt()
        loginkey = user.login(password, ip)
        user_dict = UserJsonEncoder(user, False, True).encode('dict')
        user_dict['loginkey'] = loginkey
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

    def send_email(self, email, users):
        if (self._config and self._config.email_user and
           self._config.email_password and self._config.email_server):
            sender = EmailSender(self._config.email_user,
                                 self._config.email_password,
                                 users,
                                 email,
                                 self._config.email_server)
            if not sender.send():
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def reset_user_password(self):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        username = ''
        if 'username' in self._params:
            username = self._params["username"]
        email = ''
        if 'email' in self._params:
            email = self._params["email"]
        user = self._users.get(username)
        reqid = '123456'
        if UserResetPasswordAccess(self, user, email).granted():
            request = self._reset_password_requests.add(username, email)
            reqid = request.request_id
            self.send_reset_password_email(user, request)
        return {'result': True, 'request_id': reqid}

    def validate_reset_user_password(self):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "request_id" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        request_id = self._params["request_id"]
        req = self._reset_password_requests.get(request_id)
        if not req:
            return {'result': False}
        return {'result': True}

    def change_user_password(self):
        if not self._params:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "request_id" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        if "password" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        request_id = self._params["request_id"]
        req = self._reset_password_requests.get(request_id)
        if not req:
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        user = self._users.get(req.username)
        password = self._params["password"]
        password = BcryptHash(password).encrypt()
        user.password = password
        req.accept()
        return {'result': True}

    def send_reset_password_email(self, user, request):
        email = UserResetPasswordEmail(request_id=request.request_id, server=self._server)
        self.send_email(email, [user])
