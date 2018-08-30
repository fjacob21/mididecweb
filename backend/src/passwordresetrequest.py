
class PasswordResetRequest(object):

    def __init__(self, store, request_id):
        self._store = store
        self._request_id = request_id

    def get_data(self):
        return self._store.reset_password_requests.get(self._request_id)

    def __eq__(self, value):
        return self.get_data() == value.get_data()

    @property
    def request_id(self):
        return self.get_data()['request_id']

    @property
    def date(self):
        return self.get_data()['date']

    @property
    def username(self):
        return self.get_data()['username']

    @property
    def email(self):
        return self.get_data()['email']

    @property
    def accepted(self):
        return self.get_data()['accepted']
