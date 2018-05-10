from user import USER_ACCESS_MANAGER, USER_ACCESS_SUPER


class EventAddAccess(object):

    def __init__(self, session):
        self._session = session

    def granted(self):
        if not self._session.user:
            print('No user')
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            print('is super')
            return True
        if self._session.user.access == USER_ACCESS_MANAGER:
            print('is manager')
            return True
        print(self._session.user)
        return False
