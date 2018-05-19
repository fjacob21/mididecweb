from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session
import pytest


def test_logout_user():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     user_id='test')
    user.validated = True
    loginkey = user.login('password')
    params = {}
    params['loginkey'] = loginkey
    session = Session(params, events, users, '')

    with pytest.raises(Exception):
        session.logout('')
    logout_dict = session.logout('test')
    assert logout_dict
    assert 'result' in logout_dict


def test_logout_user_bad_loginkey():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     user_id='test')
    user.validated = True
    user.login('password')
    params = {}
    params['loginkey'] = ''
    session = Session(params, events, users, '')

    with pytest.raises(Exception):
        session.logout('')
    with pytest.raises(Exception):
        session.logout('test')
