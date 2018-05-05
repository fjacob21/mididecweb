

class EventRegisterAccess(object):

    def __init__(self, session, event):
        self._session = session
        self._event = event

    def granted(self):
        if not self._session.user:
            return False
        return True
