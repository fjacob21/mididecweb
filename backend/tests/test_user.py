from src.users import Users, USER_ACCESS_SUPER, USER_ACCESS_NORMAL
from src.stores import MemoryStore


def test_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                  True, 'profile', USER_ACCESS_SUPER, True, False, '2018-04-26T13:00:00Z', 'key', 'test')
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
    assert u.lastlogin == '2018-04-26T13:00:00Z'
    assert u.loginkey == 'key'


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
