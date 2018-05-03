from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_remove_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    session = Session({}, events, users, '')

    result_dict = session.remove_event('')
    assert not result_dict
    assert len(events.list) == 1
    result_dict = session.remove_event('test')
    assert result_dict
    assert len(events.list) == 0
