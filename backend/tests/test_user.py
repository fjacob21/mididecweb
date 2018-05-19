import pytest
from src.users import Users
from src.user import USER_ACCESS_SUPER, USER_ACCESS_NORMAL
from src.stores import MemoryStore


def test_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                  True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    assert u.user_id == 'test'
    assert u.email == 'test@test.com'
    assert u.name == 'name'
    assert u.alias == 'alias'
    assert type(u.password) == str
    assert u.phone == '1234567890'
    assert u.useemail
    assert u.usesms
    assert u.profile == 'profile'
    assert u.access == USER_ACCESS_SUPER
    assert u.validated
    assert not u.smsvalidated
    assert u.lastlogin == ''
    assert u.loginkey == ''


def test_default_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw')
    assert u.email == 'test@test.com'
    assert u.name == 'name'
    assert u.alias == 'alias'
    assert type(u.password) == str
    assert u.phone == ''
    assert u.useemail
    assert not u.usesms
    assert u.profile == ''
    assert u.access == USER_ACCESS_NORMAL
    assert not u.validated
    assert not u.smsvalidated
    assert u.lastlogin == ''
    assert u.loginkey == ''
    assert u.user_id
    assert type(u.user_id) == str


def test_login():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw')
    u.validated = True
    loginkey = u.login('psw')
    assert loginkey
    assert type(loginkey) == str
    assert loginkey == u.loginkey
    assert u.lastlogin
    u.logout(loginkey)
    with pytest.raises(Exception):
        u.login('psw2')


def test_update_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                  True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')

    u.email = 'test2@test.com'
    assert u.email == 'test2@test.com'
    u.name = 'name2'
    assert u.name == 'name2'
    u.alias = 'alias2'
    assert u.alias == 'alias2'
    u.password = 'psw2'
    assert type(u.password) == str
    u.phone = '1234567891'
    assert u.phone == '1234567891'
    u.useemail = False
    assert not u.useemail
    u.usesms = False
    assert not u.usesms
    u.profile = 'profile2'
    assert u.profile == 'profile2'
    u.access = USER_ACCESS_SUPER
    assert u.access == USER_ACCESS_SUPER
    u.validated = False
    assert not u.validated
    u.smsvalidated = True
    assert u.smsvalidated
    u.lastlogin = '2'
    assert u.lastlogin == '2'
    u.loginkey = 'key'
    assert u.loginkey == 'key'
