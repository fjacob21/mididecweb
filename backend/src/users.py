from user import User
import hashlib
import random

USER_ACCESS_NORMAL = 0x1
USER_ACCESS_MANAGER = 0x3
USER_ACCESS_SUPER = 0xFF


class Users():

    def __init__(self, store):
        self._store = store

    def add(self, email, name, alias, psw, phone='', useemail=True, usesms=False,
            profile='', access=USER_ACCESS_NORMAL, validated=False, smsvalidated=False, lastlogin='', loginkey='', user_id=''):
        if not user_id:
            user_id = self.generate_user_id(email, name)
        user = self.find_email(email)
        if user:
            user_id = user.user_id
        else:
            psw = self.hash_password(psw)
            self._store.users.create(user_id, email, name, alias, psw, phone,
                                     useemail, usesms, profile, access, validated, smsvalidated, lastlogin, loginkey)
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
        user = self._store.users.get(user_id)
        if not user:
            user = self.find_email(user_id)
        if not user:
            user = self.generate_loginkey(user_id)
        if user:
            return User(self._store, user['user_id'])
        return None

    def hash_password(self, password):
        hash = hashlib.sha256()
        hash.update((password).encode())
        return hash.hexdigest()

    def generate_loginkey(self, lastlogin):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((lastlogin + salt).encode())
        return hash.hexdigest()

    def login(self, user_id, password):
        user = self.get(user_id)
        if not user:
            user = self.find_email(user_id)
        if not user:
            return None
        hpassword = self.hash_password(password)
        if hpassword == user.password:
            user.set_lastlogin()
            user.loginkey = self.generate_loginkey(user.lastlogin)
            return user.loginkey
        return None

    def logout(self, loginkey):
        user = self.find_loginkey(loginkey)
        if not user:
            return False
        user.logout()
        return True

    def change_password(self, loginkey, user_id, password):
        req_user = self.find_loginkey(loginkey)
        user = self.get(user_id)
        if not user or not req_user:
            return False
        if req_user == user or req_user.validate_access(USER_ACCESS_SUPER):
            user.password = self.hash_password(password)
