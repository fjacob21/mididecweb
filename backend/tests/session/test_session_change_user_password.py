from bcrypt_hash import BcryptHash
import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session
from src.passwordresetrequests import PasswordResetRequests


def test_request():
    store = MemoryStore()
    users = Users(store)
    pswrequests = PasswordResetRequests(store)
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
    req = pswrequests._find_pending_request('test')
    assert reset_dict
    assert 'result' in reset_dict
    assert reset_dict['result']
    params['password'] = 'toto'
    params['request_id'] = req.request_id
    session = Session(params, store)
    validate_dict = session.change_user_password()
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
    params['request_id'] = ''
    session = Session(params, store)
    with pytest.raises(Exception):
        validate_dict = session.change_user_password()
        assert validate_dict
        assert 'result' in validate_dict
        assert not validate_dict['result']
