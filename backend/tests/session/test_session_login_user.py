from bcrypt_hash import BcryptHash
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_login_user():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['password'] = 'password'
    session = Session(params, events, users, '')
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    loging_dict = session.login('')
    assert not loging_dict
    loging_dict = session.login('test')
    assert loging_dict
    assert 'user' in loging_dict


def test_login_user_bad_password():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['password'] = 'password2'
    session = Session(params, events, users, '')

    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    loging_dict = session.login('test')
    assert not loging_dict
