import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_remove_user():
    store = MemoryStore()
    users = Users(store)
    users.add('email', 'name', 'alias', 'psw', 'phone', True, True,
              user_id='test')

    session = Session({}, store, 'test')

    with pytest.raises(Exception):
        session.remove_user('')
    assert len(users.list) == 1
    result_dict = session.remove_user('test')
    assert result_dict
    assert len(users.list) == 0
    with pytest.raises(Exception):
        session.remove_user('test')
    assert len(users.list) == 0
