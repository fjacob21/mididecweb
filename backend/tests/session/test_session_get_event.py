from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_get_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    session = Session({}, events, users, '')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events = events.add('test', 'test', 30, start, dur, 'test', 'test',
                        'test@test.com', 'test')
    with pytest.raises(Exception):
        session.get_event('')
    event_dict = session.get_event('test')
    assert event_dict
    assert 'event' in event_dict
