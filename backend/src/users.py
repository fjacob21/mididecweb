from user import User
import hashlib
import random


class Users():

    def __init__(self, store):
        self._store = store

    def add(self, email, name, alias, phone='', useemail=True, usesms=False,
            profile='', validated=False, user_id=''):
        if not user_id:
            user_id = self.generate_user_id(email, name)
        self._store.users.create(user_id, email, name, alias, phone,
                                 useemail, usesms, profile, validated)
        return User(self._store, user_id)

    def generate_user_id(self, email, name):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        hash.update((email + name + salt).encode())
        return hash.hexdigest()

    def remove(self, user_id):
        self._store.users.delete(user_id)

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
        if user:
            return User(self._store, user['user_id'])
        return None
