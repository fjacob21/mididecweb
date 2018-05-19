from bcrypt_hash import BcryptHash
import pytest
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_update_user():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    params = {}
    params['email'] = 'email2'
    params['name'] = 'name2'
    params['alias'] = 'alias2'
    params['password'] = 'password2'
    params['phone'] = 'phone2'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile2'
    session = Session(params, events, users, 'test')

    with pytest.raises(Exception):
        session.update_user('')
    user_dict = session.update_user('test')
    assert user_dict
    assert 'user' in user_dict
    assert user_dict['user']['name'] == 'name2'
    user_dict = session.update_user('email2')
    assert user_dict
    assert 'user' in user_dict
    password = BcryptHash('password2', user.password.encode()).encrypt()
    loginkey = user.login(password)
    assert loginkey
    user_dict = session.update_user(loginkey)
    assert user_dict
    assert 'user' in user_dict
