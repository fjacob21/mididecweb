from user import USER_ACCESS_SUPER


class LogsAccess(object):

    def __init__(self, session):
        self._session = session

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        return False
