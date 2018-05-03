from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_remove_user():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    session = Session({}, events, users, '')

    users.add('email', 'name', 'alias', 'psw', 'phone', True, True,
              user_id='test')

    result_dict = session.remove_user('')
    assert not result_dict
    assert len(users.list) == 1
    result_dict = session.remove_user('test')
    assert result_dict
    assert len(users.list) == 0
    result_dict = session.remove_user('test')
    assert not result_dict
    assert len(users.list) == 0
