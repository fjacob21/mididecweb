
class MemoryLogins():

    def __init__(self):
        self._logins = []

    def add(self, user_id, loginkey, ip):
        login = {'user_id': user_id, 'loginkey': loginkey, 'ip': ip}
        self._logins.append(login)

    def get_user(self, user_id):
        logins = []
        for login in self._logins:
            if login['user_id'] == user_id:
                logins.append(login)
        return logins

    def get_all(self):
        return self._logins

    def get(self, loginkey):
        for login in self._logins:
            if login['loginkey'] == loginkey:
                return login
        return None

    def delete(self, loginkey):
        idx = self.index(loginkey)
        if idx != -1:
            del self._logins[idx]

    def delete_user(self, user_id):
        newlist = []
        for login in self._logins:
            if login['user_id'] != user_id:
                newlist.append(login)
        self._logins = newlist

    def reset(self):
        self._logins = []

    def clean(self):
        self.reset()

    def backup(self):
        return ('logins', self._logins)

    def restore(self, backup):
        self._logins = backup['logins']

    def index(self, loginkey):
        i = 0
        for login in self._logins:
            if login['loginkey'] == loginkey:
                return i
            i += 1
        return -1
