from user import USER_ACCESS_SUPER


class UserUpdateAccess(object):

    def __init__(self, session, user):
        self._session = session
        self._user = user

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        if self._session.user.user_id == self._user.user_id:
            return True
        return False
