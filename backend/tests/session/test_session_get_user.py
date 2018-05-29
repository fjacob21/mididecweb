import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_get_user():
    store = MemoryStore()
    users = Users(store)
    session = Session({}, store, '')

    user = users.add('email', 'name', 'alias', 'psw', 'phone', True, True,
                     user_id='test')
    user.validated = True
    with pytest.raises(Exception):
        session.get_user('')
    user_dict = session.get_user('email')
    assert user_dict
    assert 'user' in user_dict
    user_dict = session.get_user('test')
    assert user_dict
    assert 'user' in user_dict
    loginkey = user.login('psw')
    user_dict = session.get_user(loginkey)
    assert user_dict
    assert 'user' in user_dict
