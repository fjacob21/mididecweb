from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.session import Session


def test_remove_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    u = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                  access=USER_ACCESS_MANAGER, user_id='test')
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test', u)
    session = Session({}, store, 'test')

    with pytest.raises(Exception):
        session.remove_event('')
    assert len(events.list) == 1
    result_dict = session.remove_event('test')
    assert result_dict
    assert len(events.list) == 0
