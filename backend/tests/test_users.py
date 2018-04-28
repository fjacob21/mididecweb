from src.users import Users, USER_ACCESS_SUPER
from src.stores import MemoryStore


def generate_user(users):
    return users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                     True, 'profile', USER_ACCESS_SUPER, True, False, '', '', 'test')


def test_generate_user_id():
    store = MemoryStore()
    users = Users(store)
    uid = users.generate_user_id('test@test.com', 'test')
    assert uid
    assert type(uid) == str


def test_add_user():
    store = MemoryStore()
    users = Users(store)
    u = generate_user(users)
    assert u
    assert users.count == 1
    assert users.list[0] == u
    gu = users.get('test')
    assert gu
    assert gu == u
    gu = users.get('test2')
    assert not gu


def test_double_add_user():
    store = MemoryStore()
    users = Users(store)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                  True, 'profile', True)
    u2 = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                   True, 'profile', True)
    assert u
    assert u2
    assert u == u2
    assert users.count == 1
    assert users.list[0] == u


def test_remove_event():
    store = MemoryStore()
    users = Users(store)
    u = generate_user(users)
    users.remove(u.user_id)
    assert users.count == 0
    gu = users.get('test')
    assert not gu
