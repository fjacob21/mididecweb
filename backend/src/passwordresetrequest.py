import datetime


class PasswordResetRequest(object):

    def __init__(self, store, request_id):
        self._store = store
        self._request_id = request_id

    def get_data(self):
        return self._store.reset_password_requests.get(self._request_id)

    def update_data(self, data):
        self._store.reset_password_requests.update(data['request_id'],
                                                   data['date'],
                                                   data['username'],
                                                   data['email'],
                                                   data['accepted'])

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

    def accept(self):
        date = datetime.datetime.now()
        datestr = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        data = self.get_data()
        data['accepted'] = datestr
        self.update_data(data)
