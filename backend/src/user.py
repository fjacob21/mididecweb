
class User():

    def __init__(self, store, user_id):
        self._store = store
        self._user_id = user_id

    def get_data(self):
        return self._store.users.get(self._user_id)

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self.get_data()['email']

    @property
    def name(self):
        return self.get_data()['name']

    @property
    def alias(self):
        return self.get_data()['alias']

    @property
    def password(self):
        return self.get_data()['psw']

    @property
    def phone(self):
        return self.get_data()['phone']

    @property
    def useemail(self):
        return bool(self.get_data()['useemail'])

    @property
    def usesms(self):
        return bool(self.get_data()['usesms'])

    @property
    def profile(self):
        return self.get_data()['profile']

    @property
    def access(self):
        return int(self.get_data()['access'])

    @property
    def validated(self):
        return bool(self.get_data()['validated'])

    @property
    def smsvalidated(self):
        return bool(self.get_data()['smsvalidated'])

    @property
    def lastlogin(self):
        return self.get_data()['lastlogin']

    @property
    def loginkey(self):
        return self.get_data()['loginkey']

    def __eq__(self, value):
        return self.get_data() == value.get_data()
