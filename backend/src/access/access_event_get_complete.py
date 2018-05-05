from user import USER_ACCESS_MANAGER, USER_ACCESS_SUPER


class EventGetCompleteAccess(object):

    def __init__(self, session, event=None):
        self._session = session
        self._event = event

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        if not self._event:
            return False
        owner = self._session.user
        isowner = self._event.owner_id == owner.user_id
        if self._session.user.access == USER_ACCESS_MANAGER and isowner:
            return True
        return False
