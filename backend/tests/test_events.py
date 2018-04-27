from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.stores import MemoryStore


def generate_event(events):
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return events.add('test', 'test', 20, start, dur, 'test', 'test',
                      'test@test.com', 'test')


def test_generate_uid():
    start = datetime.now(pytz.timezone("America/New_York"))
    store = MemoryStore()
    events = Events(store)
    uid = events.generate_event_id(start, 'test')
    assert uid
    assert type(uid) == str


def test_add_event():
    store = MemoryStore()
    events = Events(store)
    e = generate_event(events)
    assert e
    assert events.count == 1
    assert events.list[0] == e
    ge = events.get('test')
    assert ge
    assert ge == e
    ge = events.get('test2')
    assert not ge


def test_double_add_event():
    store = MemoryStore()
    events = Events(store)
    e1 = generate_event(events)
    e2 = generate_event(events)
    assert e1
    assert e2
    assert e1 == e2
    assert events.count == 1
    assert events.list[0] == e1


def test_remove_event():
    store = MemoryStore()
    events = Events(store)
    e = generate_event(events)
    events.remove(e.event_id)
    assert events.count == 0
    ge = events.get('test')
    assert not ge
