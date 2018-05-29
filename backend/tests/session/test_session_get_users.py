from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_get_users():
    store = MemoryStore()
    users = Users(store)
    session = Session({}, store, '')

    users.add('email', 'name', 'name', '', 'phone', True, True)
    users_dict = session.get_users()
    assert users_dict
    assert 'users' in users_dict
    assert 'users' in users_dict['users']
    assert 'count' in users_dict['users']
    assert users_dict['users']['count'] == 1
    assert len(users_dict['users']['users']) == 1
