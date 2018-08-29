from datetime import datetime
import pytz
from src.stores import MemoryStore
from src.passwordresetrequests import PasswordResetRequests


def generate_request(passwordresetrequests):
    r = passwordresetrequests.add('username', 'email')
    return r


def test_add():
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    r = generate_request(passwordresetrequests)
    assert r
    assert passwordresetrequests.count == 1
    assert passwordresetrequests.list[0] == r


def test_delete():
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    r = generate_request(passwordresetrequests)
    passwordresetrequests.delete('')
    assert passwordresetrequests.count == 1
    assert passwordresetrequests.list[0] == r
    passwordresetrequests.delete(r.request_id)
    assert passwordresetrequests.count == 0


def test_get():
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    r = generate_request(passwordresetrequests)
    assert r
    assert passwordresetrequests.count == 1
    assert passwordresetrequests.get(r.request_id) == r


def test_generate_request_id():
    date = datetime.now(pytz.timezone("America/New_York"))
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    rid = passwordresetrequests.generate_request_id(date, 'username', 'email')
    assert rid
    assert type(rid) == str
