from datetime import datetime
import pytz
import hashlib
import random
from session_exception import SessionError
import errors
from random import randint


USER_ACCESS_NORMAL = 0x1
USER_ACCESS_MANAGER = 0x3
USER_ACCESS_SUPER = 0xFF


class User(object):

    def __init__(self, store, user_id):
        self._store = store
        self._user_id = user_id

    def __iter__(self):
        return self.get_data().items()

    def get_data(self):
        return self._store.users.get(self._user_id)

    def update_data(self, data):
        self._store.users.update(self._user_id, data['email'], data['name'],
                                 data['alias'], data['psw'], data['phone'],
                                 data['useemail'], data['usesms'],
                                 data['profile'], data['access'],
                                 data['validated'], data['smsvalidated'],
                                 data['lastlogin'], data['loginkey'],
                                 data['avatar_path'], data['smscode'])

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self.get_data()['email']

    @email.setter
    def email(self, value):
        data = self.get_data()
        data['email'] = value
        self.update_data(data)

    @property
    def name(self):
        return self.get_data()['name']

    @name.setter
    def name(self, value):
        data = self.get_data()
        data['name'] = value
        self.update_data(data)

    @property
    def alias(self):
        return self.get_data()['alias']

    @alias.setter
    def alias(self, value):
        data = self.get_data()
        data['alias'] = value
        self.update_data(data)

    @property
    def password(self):
        return self.get_data()['psw']

    @password.setter
    def password(self, value):
        data = self.get_data()
        data['psw'] = value
        self.update_data(data)

    @property
    def phone(self):
        return self.get_data()['phone']

    @phone.setter
    def phone(self, value):
        data = self.get_data()
        data['phone'] = value
        self.update_data(data)

    @property
    def useemail(self):
        return bool(self.get_data()['useemail'])

    @useemail.setter
    def useemail(self, value):
        data = self.get_data()
        data['useemail'] = value
        self.update_data(data)

    @property
    def usesms(self):
        return bool(self.get_data()['usesms'])

    @usesms.setter
    def usesms(self, value):
        data = self.get_data()
        data['usesms'] = value
        self.update_data(data)

    @property
    def profile(self):
        return self.get_data()['profile']

    @profile.setter
    def profile(self, value):
        data = self.get_data()
        data['profile'] = value
        self.update_data(data)

    @property
    def access(self):
        return int(self.get_data()['access'])

    @access.setter
    def access(self, value):
        data = self.get_data()
        data['access'] = value
        self.update_data(data)

    @property
    def is_normal_user(self):
        return self.access == USER_ACCESS_NORMAL

    @property
    def is_manager(self):
        return self.access == USER_ACCESS_MANAGER

    @property
    def is_super_user(self):
        return self.access == USER_ACCESS_SUPER

    @property
    def validated(self):
        return bool(self.get_data()['validated'])

    @validated.setter
    def validated(self, value):
        data = self.get_data()
        data['validated'] = value
        self.update_data(data)

    @property
    def smsvalidated(self):
        return bool(self.get_data()['smsvalidated'])

    @smsvalidated.setter
    def smsvalidated(self, value):
        data = self.get_data()
        data['smsvalidated'] = value
        self.update_data(data)

    @property
    def lastlogin(self):
        return self.get_data()['lastlogin']

    @lastlogin.setter
    def lastlogin(self, value):
        data = self.get_data()
        data['lastlogin'] = value

        self.update_data(data)

    @property
    def loginkey(self):
        return self.get_data()['loginkey']

    @loginkey.setter
    def loginkey(self, value):
        data = self.get_data()
        data['loginkey'] = value
        self.update_data(data)

    @property
    def avatar_path(self):
        return self.get_data()['avatar_path']

    @avatar_path.setter
    def avatar_path(self, value):
        data = self.get_data()
        data['avatar_path'] = value
        self.update_data(data)

    @property
    def create_date(self):
        return self.get_data()['create_date']

    @property
    def smscode(self):
        return self.get_data()['smscode']

    def set_lastlogin(self):
        lastlogin = datetime.now(pytz.timezone("America/New_York"))
        self.lastlogin = lastlogin.strftime("%Y-%m-%dT%H:%M:%SZ")

    def generate_loginkey(self, lastlogin):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((lastlogin + salt).encode())
        return hash.hexdigest()

    def generate_sms_code(self):
        data = self.get_data()
        data['smscode'] = str(randint(1000, 9999))
        self.update_data(data)
        return data['smscode']

    def validate_sms_code(self, smscode):
        if self.get_data()['smscode'] == smscode:
            self.smsvalidated = True
            return True
        raise SessionError(errors.ERROR_INVALID_SMS_CODE)

    def login(self, password, ip=''):
        if not self.validated:
            raise SessionError(errors.ERROR_VALIDATION_REQUIRED)
        if self.password == password:
            self.set_lastlogin()
            loginkey = self.generate_loginkey(self.lastlogin)
            self._store.logins.add(self.user_id, loginkey, ip)
            if not self.loginkey:
                self.loginkey = loginkey
            return loginkey
        raise SessionError(errors.ERROR_INVALID_LOGIN)

    def logout(self, loginkey):
        print('logout', self.user_id, loginkey)
        login = self._store.logins.get(loginkey)
        if not login:
            return False
        self._store.logins.delete(loginkey)
        if self.loginkey == loginkey:
            self.loginkey = ''
            logins = self._store.logins.get_user(self.user_id)
            if len(logins) > 0:
                self.loginkey = logins[0]['loginkey']
        return True

    def validate_access(self, access):
        return (self.access & access) == access

    def __eq__(self, value):
        return self.get_data() == value.get_data()
