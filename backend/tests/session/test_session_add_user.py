import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_add_user():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['name'] = 'name'
    params['alias'] = 'alias'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, store, '')

    user_dict = session.add_user()
    assert user_dict
    assert 'user' in user_dict
    assert len(users.list) == 1

    with pytest.raises(Exception):
        session.add_user()


def test_add_user_missing_email():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['name'] = 'name'
    params['alias'] = 'alias'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, store, '')

    with pytest.raises(Exception):
        session.add_user()
    assert len(users.list) == 0


def test_add_user_missing_name():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['alias'] = 'alias'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, store, '')

    with pytest.raises(Exception):
        session.add_user()
    assert len(users.list) == 0


def test_add_user_missing_alias():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['name'] = 'name'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, store, '')

    with pytest.raises(Exception):
        session.add_user()
    assert len(users.list) == 0


def test_add_user_missing_password():
    store = MemoryStore()
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['name'] = 'name'
    params['alias'] = 'alias'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, store, '')

    with pytest.raises(Exception):
        session.add_user()
    assert len(users.list) == 0
