from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.stores import MemoryStore
from src.session import Session


def test_get_event_ical():
    store = MemoryStore()
    events = Events(store)
    session = Session({}, store, '')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events = events.add('test', 'test', 30, start, dur, 'test', 'test',
                        'test@test.com', 'test')
    with pytest.raises(Exception):
        session.get_event_ical('')
    ical = session.get_event_ical('test')
    assert ical
    assert type(ical) == str
