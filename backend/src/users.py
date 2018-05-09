from user import User, USER_ACCESS_NORMAL
import hashlib
import random


class Users():

    def __init__(self, store):
        self._store = store

    def add(self, email, name, alias, psw, phone='', useemail=True,
            usesms=False, profile='', access=USER_ACCESS_NORMAL,
            validated=False, smsvalidated=False, user_id=''):
        if not user_id:
            user_id = self.generate_user_id(email, name)
        user = self.get(email)
        if user:
            user_id = user.user_id
        else:
            self._store.users.create(user_id, email, name, alias, psw, phone,
                                     useemail, usesms, profile, access,
                                     validated, smsvalidated, '', '')
        return User(self._store, user_id)

    def generate_user_id(self, email, name):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((email + name + salt).encode())
        return hash.hexdigest()

    def remove(self, user_id):
        self._store.users.delete(user_id)

    def find_email(self, email):
        for user in self.list:
            if user.email == email:
                return user
        return None

    def find_alias(self, alias):
        for user in self.list:
            if user.alias == alias:
                return user
        return None

    def find_loginkey(self, loginkey):
        for user in self.list:
            if user.loginkey == loginkey:
                return user
        return None

    @property
    def list(self):
        result = []
        users = self._store.users.get_all()
        for user in users:
            result.append(User(self._store, user['user_id']))
        return result

    @property
    def count(self):
        return len(self.list)

    def get(self, user_id):
        if not user_id:
            return None
        user = self._store.users.get(user_id)
        if user:
            return User(self._store, user['user_id'])
        if not user:
            user = self.find_email(user_id)
        if not user:
            user = self.find_alias(user_id)
        if not user:
            user = self.find_loginkey(user_id)
        return user
