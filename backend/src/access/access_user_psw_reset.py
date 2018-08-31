

class UserResetPasswordAccess(object):

    def __init__(self, session, user, email):
        self._session = session
        self._user = user
        self._email = email

    def granted(self):
        if not self._user:
            return False
        if self._user.email == self._email:
            return True
        return False
