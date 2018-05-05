from user import USER_ACCESS_MANAGER, USER_ACCESS_SUPER


class UserGetCompleteAccess(object):

    def __init__(self, session, user=None):
        self._session = session
        self._user = user

    def granted(self):
        if not self._session.user:
            return False
        if self._session.user.access == USER_ACCESS_SUPER:
            return True
        if not self._user:
            return False
        events = self._session.events
        owner = self._session.user
        isowner = events.is_user_attending_owning_events(owner, self._user)
        if self._session.user.access == USER_ACCESS_MANAGER and isowner:
            return True
        if self._session.user.user_id == self._user.user_id:
            return True
        return False
