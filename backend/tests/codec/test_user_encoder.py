from src.codec.user_json_encoder import UserJsonEncoder
from src.users import Users
from src.user import USER_ACCESS_SUPER
import json
from src.stores import MemoryStore


def test_complete_user_json_encoder():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonobj = UserJsonEncoder(u, True).encode('dict')
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert jsonobj['email'] == "test@test.com"
    assert jsonobj['password'] == "psw"
    assert jsonobj['phone'] == '1234567890'
    assert jsonobj['useemail']
    assert jsonobj['usesms']
    assert jsonobj['profile'] == 'profile'
    assert jsonobj['access'] == USER_ACCESS_SUPER
    assert jsonobj['validated']
    assert not jsonobj['smsvalidated']
    assert jsonobj['lastlogin'] == ''
    assert jsonobj['loginkey'] == ''


def test_user_json_encoder():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonobj = UserJsonEncoder(u).encode('dict')
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert 'email' not in jsonobj
    assert 'password' not in jsonobj
    assert 'phone' not in jsonobj
    assert 'useemail' not in jsonobj
    assert 'usesms' not in jsonobj
    assert 'profile' not in jsonobj
    assert 'access' not in jsonobj
    assert 'validated' not in jsonobj
    assert 'smsvalidated' not in jsonobj
    assert 'lastlogin' not in jsonobj
    assert 'loginkey' not in jsonobj


def test_login_user_json_encoder():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonobj = UserJsonEncoder(u, False, True).encode('dict')
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert jsonobj['access'] == USER_ACCESS_SUPER
    assert jsonobj['loginkey'] == ''
    assert 'email' not in jsonobj
    assert 'password' not in jsonobj
    assert 'phone' not in jsonobj
    assert 'useemail' not in jsonobj
    assert 'usesms' not in jsonobj
    assert 'profile' not in jsonobj
    assert 'validated' not in jsonobj
    assert 'smsvalidated' not in jsonobj
    assert 'lastlogin' not in jsonobj


def test_complete_user_json_encoder_string():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonstr = UserJsonEncoder(u, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert jsonobj['email'] == "test@test.com"
    assert jsonobj['password'] == "psw"
    assert jsonobj['phone'] == '1234567890'
    assert jsonobj['useemail']
    assert jsonobj['usesms']
    assert jsonobj['profile'] == 'profile'
    assert jsonobj['access'] == USER_ACCESS_SUPER
    assert jsonobj['validated']
    assert not jsonobj['smsvalidated']
    assert jsonobj['lastlogin'] == ''
    assert jsonobj['loginkey'] == ''


def test_user_json_encoder_string():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonstr = UserJsonEncoder(u).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert 'email' not in jsonobj
    assert 'password' not in jsonobj
    assert 'phone' not in jsonobj
    assert 'useemail' not in jsonobj
    assert 'usesms' not in jsonobj
    assert 'profile' not in jsonobj
    assert 'access' not in jsonobj
    assert 'validated' not in jsonobj
    assert 'smsvalidated' not in jsonobj
    assert 'lastlogin' not in jsonobj
    assert 'loginkey' not in jsonobj


def test_login_user_json_encoder_string():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    jsonstr = UserJsonEncoder(u, False, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert jsonobj['access'] == USER_ACCESS_SUPER
    assert jsonobj['loginkey'] == ''
    assert 'email' not in jsonobj
    assert 'password' not in jsonobj
    assert 'phone' not in jsonobj
    assert 'useemail' not in jsonobj
    assert 'usesms' not in jsonobj
    assert 'profile' not in jsonobj
    assert 'validated' not in jsonobj
    assert 'smsvalidated' not in jsonobj
    assert 'lastlogin' not in jsonobj
