from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_get_events():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    session = Session({}, events, users, '')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events = events.add('test', 'test', 30, start, dur, 'test', 'test',
                        'test@test.com', 'test')
    events_dict = session.get_events()
    assert events_dict
    assert 'events' in events_dict
    assert 'events' in events_dict['events']
    assert 'count' in events_dict['events']
    assert events_dict['events']['count'] == 1
    assert len(events_dict['events']['events']) == 1
