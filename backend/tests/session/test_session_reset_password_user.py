from bcrypt_hash import BcryptHash
from src.users import Users
from src.stores import MemoryStore
from src.session import Session
from src.user import USER_ACCESS_SUPER


def test_reset_password_user():
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
    session = Session(params, store, 'test')
    reset_dict = session.reset_user_password()
    assert reset_dict
    assert 'result' in reset_dict
    assert reset_dict['result']
    assert 'request_id' in reset_dict
    assert reset_dict['request_id'] != '123456'


def test_invalid_user():
    store = MemoryStore()
    users = Users(store)
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, 'phone', True, True,
                     user_id='test')
    user.validated = True
    params = {}
    params['username'] = 'test'
    params['email'] = 'email'
    params['loginkey'] = ''
    session = Session(params, store)
    reset_dict = session.reset_user_password()
    assert reset_dict
    assert 'result' in reset_dict
    assert reset_dict['result']
    assert 'request_id' in reset_dict
    assert reset_dict['request_id'] == '123456'


def test_admin_user():
    store = MemoryStore()
    users = Users(store)
    password = BcryptHash('password').encrypt()
    useradmin = users.add('email', 'name', 'alias', password, 'phone', True,
                          True, access=USER_ACCESS_SUPER,  user_id='test')
    useradmin.validated = True
    user = users.add('emailuser', 'nameuser', 'aliasuser', password, 'phone',
                     True, True,
                     user_id='testuser')
    user.validated = True
    params = {}
    params['username'] = 'nameuser'
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
