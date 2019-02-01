from codec import EventJsonEncoder, EventsJsonEncoder
from codec import UsersJsonEncoder, UserJsonEncoder, LogsJsonEncoder
from codec import EventPresencesPdfEncoder
from datetime import datetime, timedelta
from email_sender import EmailSender
from sms_sender import SmsSender
from eventtextgenerator import EventTextGenerator
from email_generators import iCalGenerator
from bcrypt_hash import BcryptHash
from access import UserAddAccess, UserGetCompleteAccess, UserUpdateAccess
from access import UserRemoveAccess, EventGetCompleteAccess, EventAddAccess
from access import EventRemoveAccess, EventRegisterAccess, EventPublishAccess
from access import EventUpdateAccess, UserResetPasswordAccess, LogsAccess
from access import EventPresencesAccess
from event import ATTENDEE_LIST, WAITING_LIST
from jinja2 import Environment, FileSystemLoader
from session_exception import SessionError
import errors
import os
from events import Events
from event import Event
from users import Users
from logs import Logs
from passwordresetrequests import PasswordResetRequests
from email_generators import UserValidationEmail, EventPublishEmail
from email_generators import UserPromoteEmail, UserEventConfirmEmail
from email_generators import EventDateChangedEmail, EventLocationChangedEmail
from email_generators import UserEventWaitEmail, UserResetPasswordEmail
from flask import make_response
import logger


class Session(object):

    def __init__(self, params, store, loginkey='', config=None,
                 server='https://mididecouverte.org/'):
        self._params = params
        self._store = store
        self._loginkey = loginkey
        self._events = Events(store)
        self._users = Users(store)
        self._logs = Logs(store)
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

    def get_logs(self):
        logger.get().info('Get logs')
        if not LogsAccess(self).granted():
            logger.get().error('Get logs access denied login:{0}'.format(self._user.user_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        logs_dict = LogsJsonEncoder(self._logs).encode('dict')
        browsers = {}
        cities = {}
        oss = {}
        logger.get().info('process logs')
        for log in self._logs.list:
            if log.browser not in browsers:
                browsers[log.browser] = {'count': 1, 'versions':
                                         {log.browser_version: 1},
                                         'city': [log.city]}
            else:
                browsers[log.browser]['count'] += 1
                if log.browser_version not in browsers[log.browser]['versions']:
                    browsers[log.browser]['versions'][log.browser_version] = 1
                else:
                    browsers[log.browser]['versions'][log.browser_version] += 1
                browsers[log.browser]['city'].append(log.city)
            if log.city not in cities:
                cities[log.city] = 1
            else:
                cities[log.city] += 1
            if log.os not in oss:
                oss[log.os] = {'count': 1, 'versions': {log.os_version: 1}}
            if log.os_version not in oss[log.os]['versions']:
                oss[log.os]['versions'][log.os_version] = 1
            else:
                oss[log.os]['versions'][log.os_version] += 1
        return {'logs': logs_dict, 'browsers': browsers, 'cities': cities,
                'os': oss}

    def get_event_presences(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Get event presences invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventPresencesAccess(self, event).granted():
            logger.events().error('Get event presences access denied login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)

        user = self._users.get(event.organizer_name)
        pdfcodec = EventPresencesPdfEncoder(event, user)
        p = pdfcodec.encode()
        response = make_response(p)
        response.headers.set('Content-Type', 'application/pdf')
        return response

    def get_events(self):
        complete = EventGetCompleteAccess(self).granted()
        events_dict = EventsJsonEncoder(self._events, complete).encode('dict')
        return {'events': events_dict}

    def get_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Get event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        complete = EventGetCompleteAccess(self, event).granted()
        show_details = False
        if self.user:
            show_details = True
        event_dict = EventJsonEncoder(event, complete, show_details, show_details).encode('dict')
        return {'event': event_dict}

    def get_event_ical(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Get event ical invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        return iCalGenerator(event).generate()

    def get_event_jinja(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Get event jinja invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
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
            logger.events().error('Add event missing params login:{0} event:{1}'.format(self._user.user_id, self._params["title"]))
            raise SessionError(errors.ERROR_MISSING_PARAMS)

        if not EventAddAccess(self).granted():
            logger.events().error('Add event access denied login:{0} event:{1}'.format(self._user.user_id, self._params["title"]))
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
        not_training = ''
        if "not_training" in self._params:
            not_training = self._params["not_training"]
        e = self._events.add(title, description, max_attendee, start, duration,
                             location, organizer_name, organizer_email,
                             event_id, self._user, not_training)
        return {'event': EventJsonEncoder(e, True).encode('dict')}

    def remove_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Remove event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventRemoveAccess(self, event).granted():
            logger.events().error('Remove event access denied login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        self._events.remove(event_id)
        return {'result': True}

    def update_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Update event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventUpdateAccess(self, event).granted():
            logger.events().error('Update event access denied login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        max_attendee = event.max_attendee
        if 'max_attendee' in self._params:
            max_attendee = int(self._params['max_attendee'])
        if max_attendee < event.max_attendee and max_attendee < len(event.all_attendees):
            logger.events().error('Update event attendee too low login:{0} event:{1} max:{2} attendees:{3}'.format(self._user.user_id, event_id, max_attendee, len(event.all_attendees)))
            raise SessionError(errors.ERROR_ATTENDEE_TOO_LOW)

        old_event = event.get_data()
        old_event = Event(self._store, event_id, static_data=old_event)
        date_changed = False
        location_changed = False
        if max_attendee > event.max_attendee:
            current_max_attendee = event.max_attendee
            event.max_attendee = max_attendee
            promotees = event.promote_waitings(max_attendee - current_max_attendee)
            for promotee in promotees:
                logger.events().info('Send email to promotee {0} for event {1}'.format(promotee.user_id, event_id))
                self.send_promotee_email(event, promotee)
        event.max_attendee = max_attendee
        if 'title' in self._params:
            event.title = self._params['title']
        if 'description' in self._params:
            event.description = self._params['description']
        if 'not_training' in self._params:
            logger.events().info('Update not training field')
            event.not_training = self._params['not_training']
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
            logger.events().error('Register event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            logger.events().error('Register event invalid request login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not EventRegisterAccess(self, event).granted():
            logger.get().error('Register event access denied login:{0} event:{1}'.format(self._user.user_id, event_id))
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
            logger.events().error('Unregister event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            logger.events().error('Unregister event invalid request login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not self.user:
            logger.events().error('Unregister event need to be login login:{0} event:{1}'.format(self._user.user_id, event_id))
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

    def present_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Present event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            logger.events().error('Present event invalid request login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not EventPublishAccess(self, event).granted():
            logger.get().error('Present event access denied login:{0} event:{1} user:{2}'.format(self._user.user_id, event_id, self._params["user_id"]))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if "user_id" not in self._params or "present" not in self._params:
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        user_id = self._params["user_id"]
        present = self._params["present"]
        logger.get().info('Present {1} user {0} at event {2}'.format(user_id, present, event_id))
        user = self._users.get(user_id)
        if not user:
            raise SessionError(errors.ERROR_INVALID_USER)
        result = event.present_attendee(user, present)
        return {'result': result,
                'event': EventJsonEncoder(event, True).encode('dict')}

    def publish_event(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Publish event invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventPublishAccess(self, event).granted():
            logger.get().error('Publish event access denied login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if not self._params:
            logger.events().error('Publish event invalid request login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        self.send_publish_event_email(event)
        self.send_publish_event_sms(event)
        return {'result': True}

    def send_publish_event_email(self, event):
        email = EventPublishEmail(event=event, server=self._server)
        users = [user for user in self._users.list if not event.is_attending(user)]
        self.send_email(email, users)

    def send_publish_event_sms(self, event):
        if self._config and self._config.sms_sid and self._config.sms_token:
            body = EventTextGenerator(event, False).generate()
            res = True
            users = [user for user in self._users.list if not event.is_attending(user)]
            for user in users:
                if (user.usesms and user.phone and user.validated and
                   user.smsvalidated):
                    sender = SmsSender(self._config.sms_sid,
                                       self._config.sms_token, user.phone,
                                       event.title, body)
                    res = sender.send()
            if not res:
                logger.events().error('Publish event send sms login:{0} event:{1}'.format(self._user.user_id, event.event_id))
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def get_event_attachment(self, event_id, attachment):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Get event attachment invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        event_path = '../data/events/' + event.event_id
        attachment_path = event_path + '/' + attachment
        aidx = event.find_attachment(attachment_path)
        if aidx == -1:
            raise SessionError(errors.ERROR_INVALID_ATTACHMENT)
        return event.attachments[aidx]

    def add_event_attachment(self, event_id, attachment):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Add event attachment invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not EventUpdateAccess(self, event).granted():
            logger.get().error('Add event attachment access denied login:{0} event:{1} attachment:{2}'.format(self._user.user_id, event_id, attachment.filename))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        event_path = '../data/events/' + event.event_id
        attachment_path = event_path + '/' + attachment.filename
        os.makedirs(event_path, exist_ok=True)
        attachment.save(attachment_path)
        event.add_attachment(attachment_path)
        return {'result': True}

    def remove_event_attachment(self, event_id):
        event = self._events.get(event_id)
        if not event:
            logger.events().error('Remove event attachment invalid event login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_EVENT)
        if not self._params:
            logger.events().error('Remove event attachment invalid request login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not EventUpdateAccess(self, event).granted():
            logger.get().error('Remove event attachment access denied login:{0} event:{1} attachment:{2}'.format(self._user.user_id, event_id, self._params['attachment']))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if 'attachment' not in self._params:
            logger.events().error('Remove event invalid request missing attachment field login:{0} event:{1}'.format(self._user.user_id, event_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        attachment = self._params['attachment']
        event_path = '../data/events/' + event.event_id
        attachment_path = event_path + '/' + attachment
        event.remove_attachment(attachment_path)
        os.remove(attachment_path)
        return {'result': True}

    def get_users(self):
        complete = UserGetCompleteAccess(self).granted()
        users_dict = UsersJsonEncoder(self._users, complete).encode('dict')
        return {'users': users_dict}

    def get_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Get user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        complete = UserGetCompleteAccess(self, user).granted()
        user_dict = UserJsonEncoder(user, complete).encode('dict')
        return {'user': user_dict}

    def get_user_avatar(self, user_id):
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Get user avatar invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not user.avatar_path:
            logger.users().error('Get user avatar no avatar login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_NO_AVATAR)
        return user.avatar_path

    def add_user(self):
        if not self._params:
            logger.users().error('Add user invalid request login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if ('email' not in self._params or
            'name' not in self._params or
            'alias' not in self._params or
           'password' not in self._params):
            logger.users().error('Add user invalid request missing fields login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)

        if not UserAddAccess(self).granted():
            logger.users().error('Add user access denied login:{0}'.format(self._user.user_id))
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
            logger.users().error('Add user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        user = self._users.get(alias)
        if user:
            logger.users().error('Add user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
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
            logger.users().error('Validate user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        user.validated = True
        env = Environment(loader=FileSystemLoader('emails'))
        t = env.get_template('uservalidated.html')
        return t.render(user=user, server=self._server)

    def sendcode(self, user_id):
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Send user code invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserAddAccess(self).granted():
            logger.users().error('Send user code access denied login:{0} user:{1}'.format(self._user.user_id, user_id))
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
                logger.users().error('Send user sms code login:{0} user:{1}'.format(self._user.user_id, user.user_id))
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def validatecode(self, user_id):
        if not self._params:
            logger.users().error('Validate user code invalid request login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Validate user code invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserAddAccess(self).granted():
            logger.users().error('Validate user code access denied login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if 'smscode' not in self._params:
            logger.users().error('Validate user code invalid request missing smscode field login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        smscode = self._params["smscode"]
        return {'result': user.validate_sms_code(smscode)}

    def validate_user_info(self):
        if not self._params:
            logger.users().error('Validate user info invalid request login:{0}'.format(self._user.user_id))
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
            logger.users().error('Remove user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserRemoveAccess(self, user).granted():
            logger.get().error('Remove user access denied login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        if user.avatar_path:
            os.remove(user.avatar_path)
        self._users.remove(user.user_id)
        return {'result': True}

    def update_user(self, user_id):
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Update user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserUpdateAccess(self, user).granted():
            logger.get().error('Update user access denied login:{0} user:{1}'.format(self._user.user_id, user_id))
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
            logger.users().error('Update user avatar invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_USER)
        if not UserUpdateAccess(self, user).granted():
            logger.get().error('Update user avatar access denied login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_ACCESS_DENIED)
        avatar_path = '../data/img/users/' + user.user_id + '.jpg'
        user.avatar_path = avatar_path
        avatar.save(avatar_path)
        return {'result': True}

    def login(self, user_id, ip=''):
        if not self._params:
            logger.users().error('Login user invalid request login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "password" not in self._params:
            logger.users().error('Login user invalid request missing password field login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        password = self._params["password"]
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Login user invalid login login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_LOGIN)
        register = ''
        event = None
        if 'register' in self._params:
            register = self._params['register']
            event = self._events.get(register)
            if not event:
                logger.events().error('Register user to event invalid event login:{0} user:{1} event:{2}'.format(self._user.user_id, user_id, register))
                raise SessionError(errors.ERROR_INVALID_EVENT)
        password = BcryptHash(password, user.password.encode()).encrypt()
        loginkey = user.login(password, ip)
        user_dict = UserJsonEncoder(user, False, True).encode('dict')
        user_dict['loginkey'] = loginkey
        if event:
            print('register', register)
            event.register_attendee(user)
            return {'user': user_dict, 'register': register}
        return {'user': user_dict}

    def logout(self, user_id):
        if not self._params:
            logger.users().error('Logout user invalid request login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "loginkey" not in self._params:
            logger.users().error('Logout user invalid request missing loginkey login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        loginkey = self._params["loginkey"]
        user = self._users.get(user_id)
        if not user:
            logger.users().error('Logout user invalid user login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if not user.logout(loginkey):
            logger.users().error('Logout user invalid loginkey login:{0} user:{1}'.format(self._user.user_id, user_id))
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
                logger.users().error('Send user email login:{0}'.format(self._user.user_id))
                raise SessionError(errors.ERROR_SENDING_EMAIL)

    def reset_user_password(self):
        if not self._params:
            logger.users().error('Reset user password invalid request login:{0}'.format(self._user.user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        username = ''
        if 'username' in self._params:
            username = self._params["username"]
        email = ''
        if 'email' in self._params:
            email = self._params["email"]
        user = self._users.get(username)
        if UserResetPasswordAccess(self, user, email).granted():
            request = self._reset_password_requests.add(username, email)
            self.send_reset_password_email(user, request)
        return {'result': True}

    def validate_reset_user_password(self):
        if not self._params:
            logger.users().error('Validate user reset password invalid request login:{0}'.format(self._user.user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "request_id" not in self._params:
            logger.users().error('Validate user reset password invalid request missing request_id field login:{0}'.format(self._user.user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        request_id = self._params["request_id"]
        req = self._reset_password_requests.get(request_id)
        if not req or req.accepted:
            return {'result': False}
        return {'result': True}

    def change_user_password(self):
        if not self._params:
            logger.users().error('Change user password invalid request login:{0}'.format(self._user.user_id))
            raise SessionError(errors.ERROR_INVALID_REQUEST)
        if "request_id" not in self._params:
            logger.users().error('Change user password invalid request missing request_id field login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        if "password" not in self._params:
            logger.users().error('Change user password invalid request missing password field login:{0} user:{1}'.format(self._user.user_id, user_id))
            raise SessionError(errors.ERROR_MISSING_PARAMS)
        request_id = self._params["request_id"]
        req = self._reset_password_requests.get(request_id)
        if not req:
            logger.users().error('Change user password invalid request not a valid request login:{0} user:{1}'.format(self._user.user_id, user_id))
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
