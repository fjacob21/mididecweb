from src.users import Users
from src.stores import MemoryStore


def test_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', '1234567890', True,
                  True, 'profile', True, 'test')
    assert u.user_id == 'test'
    assert u.email == 'test@test.com'
    assert u.name == 'name'
    assert u.alias == 'alias'
    assert u.phone == '1234567890'
    assert u.useemail
    assert u.usesms
    assert u.profile == 'profile'
    assert u.validated


def test_default_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias')
    assert u.email == 'test@test.com'
    assert u.name == 'name'
    assert u.alias == 'alias'
    assert u.phone == ''
    assert u.useemail
    assert not u.usesms
    assert u.profile == ''
    assert not u.validated
    assert u.user_id
    assert type(u.user_id) == str
