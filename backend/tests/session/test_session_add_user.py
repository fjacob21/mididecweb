from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_add_user():
    store = MemoryStore()
    events = Events(store)
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
    session = Session(params, events, users, '')

    user_dict = session.add_user()
    assert user_dict
    assert 'user' in user_dict
    assert len(users.list) == 1

    user_dict = session.add_user()
    assert not user_dict


def test_add_user_missing_email():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['name'] = 'name'
    params['alias'] = 'alias'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, events, users, '')

    user_dict = session.add_user()
    assert not user_dict
    assert len(users.list) == 0


def test_add_user_missing_name():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['alias'] = 'alias'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, events, users, '')

    user_dict = session.add_user()
    assert not user_dict
    assert len(users.list) == 0


def test_add_user_missing_alias():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['name'] = 'name'
    params['password'] = 'password'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, events, users, '')

    user_dict = session.add_user()
    assert not user_dict
    assert len(users.list) == 0


def test_add_user_missing_password():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['email'] = 'email'
    params['name'] = 'name'
    params['alias'] = 'alias'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True
    params['profile'] = 'profile'
    session = Session(params, events, users, '')

    user_dict = session.add_user()
    assert not user_dict
    assert len(users.list) == 0
