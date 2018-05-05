

class UserAddAccess(object):

    def __init__(self, session):
        self._session = session

    def granted(self):
        return True
