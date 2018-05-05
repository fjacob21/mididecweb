from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.stores import MemoryStore
from src.users import Users
from src.user import USER_ACCESS_MANAGER, USER_ACCESS_NORMAL


def generate_event(events, users):
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    u = users.add("test@test.com", 'name', 'alias', 'psw',
                  access=USER_ACCESS_MANAGER, user_id='test')
    a = users.add("test2@test.com", 'attendee', 'alias', 'psw',
                  access=USER_ACCESS_NORMAL, user_id='attendee')
    e = events.add('test', 'test', 20, start, dur, 'test', 'test',
                   'test@test.com', 'test', u)
    e.register_attendee(a)
    return e


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
    users = Users(store)
    e = generate_event(events, users)
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
    users = Users(store)
    e1 = generate_event(events, users)
    e2 = generate_event(events, users)
    assert e1
    assert e2
    assert e1 == e2
    assert events.count == 1
    assert events.list[0] == e1


def test_remove_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    e = generate_event(events, users)
    events.remove(e.event_id)
    assert events.count == 0
    ge = events.get('test')
    assert not ge


def test_find_owning_events():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    e = generate_event(events, users)
    owner = users.get('test')
    owning_events = events.find_owning_events(owner)
    assert owning_events
    assert len(owning_events) == 1
    assert e == owning_events[0]


def test_is_user_attending_owning_events():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    generate_event(events, users)
    owner = users.get('test')
    attendee = users.get('attendee')
    assert events.is_user_attending_owning_events(owner, attendee)
    assert not events.is_user_attending_owning_events(owner, owner)
