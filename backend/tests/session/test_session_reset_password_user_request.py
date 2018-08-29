from bcrypt_hash import BcryptHash
import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_request():
    store = MemoryStore()
    users = Users(store)
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    params = {}
    params['username'] = 'test'
    params['email'] = 'email'
    params['password'] = 'password'
    session = Session(params, store)
    loging_dict = session.login('test')
    params['loginkey'] = loging_dict['user']['loginkey']
    session = Session(params, store)
    reset_dict = session.reset_user_password()
    assert reset_dict
    assert 'result' in reset_dict
    assert reset_dict['result']
    assert 'request_id' in reset_dict
    assert reset_dict['request_id']
    params['password'] = 'toto'
    validate_dict = session.user_password_reset_request('test', reset_dict['request_id'])
    assert validate_dict
    assert 'result' in validate_dict
    assert validate_dict['result']


def test_invalid_request():
    store = MemoryStore()
    users = Users(store)
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    params = {}
    params['username'] = 'test'
    params['email'] = 'email'
    params['password'] = 'password'
    session = Session(params, store)
    loging_dict = session.login('test')
    params['loginkey'] = loging_dict['user']['loginkey']
    session = Session(params, store)
    reset_dict = session.reset_user_password()
    assert reset_dict
    assert 'result' in reset_dict
    assert reset_dict['result']
    assert 'request_id' in reset_dict
    assert reset_dict['request_id']
    with pytest.raises(Exception):
        validate_dict = session.user_password_reset_request('name', '')
        assert validate_dict
        assert 'result' in validate_dict
        assert not validate_dict['result']
