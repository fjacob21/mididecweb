from user import USER_ACCESS_MANAGER, USER_ACCESS_SUPER


class EventAddAccess(object):

    def __init__(self, session):
        self._session = session

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        if self._session.user.access == USER_ACCESS_MANAGER:
            return True
        return False
