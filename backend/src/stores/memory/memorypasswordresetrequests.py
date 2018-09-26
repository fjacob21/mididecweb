

class MemoryPasswordResetRequests():

    def __init__(self):
        self._requests = []

    def create(self, request_id, date, username, email):
        if not self.get(request_id):
            obj = self.create_object(request_id, date, username, email)
            self._requests.append(obj)
            return obj

    def get_all(self):
        return self._requests

    def get(self, request_id):
        for request in self._requests:
            if request['request_id'] == request_id:
                return request
        return None

    def update(self, request_id, date, username, email, accepted):
        req = self.get(request_id)
        if req:
            obj = self.create_object(request_id, date, username,
                                     email, accepted)
            self._requests[self.index(request_id)] = obj

    def delete(self, request_id):
        idx = self.index(request_id)
        if idx != -1:
            del self._requests[idx]

    def reset(self):
        self._requests = []

    def clean(self):
        self.reset()

    def backup(self):
        return ('reset_password_requests', self._requests)

    def restore(self, backup):
        self._requests = backup['reset_password_requests']

    def create_object(self, request_id, date, username, email, accepted=''):
        request = {}
        request['request_id'] = request_id
        request['date'] = date
        request['username'] = username
        request['email'] = email
        request['accepted'] = accepted
        return request

    def index(self, request_id):
        i = 0
        for request in self._requests:
            if request['request_id'] == request_id:
                return i
            i += 1
        return -1
