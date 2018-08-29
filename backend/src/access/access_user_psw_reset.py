from user import USER_ACCESS_SUPER


class UserResetPasswordAccess(object):

    def __init__(self, session, user, email):
        self._session = session
        self._user = user
        self._email = email

    def granted(self):
        print('access', self._session.user, self._user)
        if not self._session.user or not self._user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        if (self._session.user.user_id == self._user.user_id
            and self._user.email == self._email):
            return True
        return False
