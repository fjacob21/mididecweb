from datetime import datetime, timedelta
import pytz
from bcrypt_hash import BcryptHash
import pytest
from src.users import Users
from src.events import Events
from src.stores import MemoryStore
from src.session import Session


def test_login_user():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['password'] = 'password'
    session = Session(params, store, '')
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    with pytest.raises(Exception):
        session.login('')
    loging_dict = session.login('test')
    assert loging_dict
    assert 'user' in loging_dict


def test_login_user_bad_password():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['password'] = 'password2'
    session = Session(params, store, '')

    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    with pytest.raises(Exception):
        session.login('test')


def test_login_user_register():
    store = MemoryStore()
    users = Users(store)
    events = Events(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)

    params = {}
    params['password'] = 'password'
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test', user)
    user.validated = True
    params['register'] = 'test'
    session = Session(params, store, '')
    loging_dict = session.login('test')
    assert loging_dict
    assert 'user' in loging_dict
    assert 'register' in loging_dict
    assert loging_dict['register'] == 'test'


def test_login_user_register_bad_event():
    store = MemoryStore()
    users = Users(store)
    events = Events(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)

    params = {}
    params['password'] = 'password'
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test', user)
    user.validated = True
    params['register'] = ''
    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.login('test')
