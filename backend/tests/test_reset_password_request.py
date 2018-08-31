from src.passwordresetrequests import PasswordResetRequests
from src.stores import MemoryStore


def generate_request(passwordresetrequests):
    r = passwordresetrequests.add('username', 'email')
    return r


def test_item():
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    r = generate_request(passwordresetrequests)
    assert r.username == "username"
    assert r.email == "email"
    assert r.request_id
    assert r.date
    assert r.accepted == ''


def test_accepted():
    store = MemoryStore()
    passwordresetrequests = PasswordResetRequests(store)
    r = generate_request(passwordresetrequests)
    assert r.username == "username"
    assert r.email == "email"
    assert r.request_id
    assert r.date
    assert r.accepted == ''
    r.accept()
    assert r.accepted
