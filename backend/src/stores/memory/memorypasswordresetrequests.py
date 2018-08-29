

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

    def delete(self, request_id):
        idx = self.index(request_id)
        if idx != -1:
            del self._requests[idx]

    def reset(self):
        self._requests = []

    def clean(self):
        self.reset()

    def create_object(self, request_id, date, username, email):
        request = {}
        request['request_id'] = request_id
        request['date'] = date
        request['username'] = username
        request['email'] = email
        return request

    def index(self, request_id):
        i = 0
        for request in self._requests:
            if request['request_id'] == request_id:
                return i
            i += 1
        return -1
