from datetime import datetime
import pytz


class User(object):

    def __init__(self, store, user_id):
        self._store = store
        self._user_id = user_id

    def get_data(self):
        return self._store.users.get(self._user_id)

    def update_data(self, data):
        self._store.users.update(self._user_id, data['email'], data['name'], data['psw'], data['alias'],
                                 data['phone'], data['useemail'], data['usesms'], data['profile'],
                                 data['access'], data['validated'], data['smsvalidated'], data['lastlogin'],
                                 data['loginkey'])

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
    def validated(self):
        return bool(self.get_data()['validated'])

    @validated.setter
    def validated(self, value):
        data = self.get_data()
        data['valdated'] = value
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

    def set_lastlogin(self):
        lastlogin = datetime.now(pytz.timezone("America/New_York"))
        self.lastlogin = lastlogin.strftime("%Y-%m-%dT%H:%M:%SZ")

    def logout(self):
        self.loginkey = ''

    def validate_access(self, access):
        return (self.access & access) == access

    def __eq__(self, value):
        return self.get_data() == value.get_data()
