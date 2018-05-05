from user import USER_ACCESS_SUPER, USER_ACCESS_MANAGER


class EventPublishAccess(object):

    def __init__(self, session, event):
        self._session = session
        self._event = event

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        is_owner = self._event.owner_id == self._session.user.user_id
        if self._session.user.access == USER_ACCESS_MANAGER and is_owner:
            return True
        return False
