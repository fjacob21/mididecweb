import datetime
from passwordresetrequest import PasswordResetRequest
import hashlib
import random


class PasswordResetRequests(object):

    def __init__(self, store):
        self._store = store

    def add(self, username, email):
        req = self._find_pending_request(username)
        if not req:
            date = datetime.datetime.now()
            datestr = date.strftime("%Y-%m-%dT%H:%M:%SZ")
            request_id = self.generate_request_id(date, username, email)
            self._store.reset_password_requests.create(request_id, datestr,
                                                       username, email)
        else:
            request_id = req.request_id
        return PasswordResetRequest(self._store, request_id)

    def generate_request_id(self, date, username, email):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        datestr = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        hash.update((datestr + username + email + salt).encode())
        return hash.hexdigest()

    def delete(self, request_id):
        self._store.reset_password_requests.delete(request_id)

    def get(self, request_id):
        req = self._store.reset_password_requests.get(request_id)
        if not req:
            return None
        return PasswordResetRequest(self._store, req['request_id'])

    def _find_pending_request(self, username):
        for req in self.list:
            if req.username == username and not req.accepted:
                return req
        return None

    @property
    def list(self):
        result = []
        reset_password_requests = self._store.reset_password_requests.get_all()
        for reset_password_request in reset_password_requests:
            result.append(PasswordResetRequest(self._store, reset_password_request['request_id']))
        return result

    @property
    def count(self):
        return len(self.list)
