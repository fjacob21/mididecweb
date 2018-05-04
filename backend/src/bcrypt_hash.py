import bcrypt


class BcryptHash(object):

    def __init__(self, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        self._password = password
        self._salt = salt

    def encrypt(self):
        hash = bcrypt.hashpw(self._password.encode(), self._salt).decode()
        return hash
