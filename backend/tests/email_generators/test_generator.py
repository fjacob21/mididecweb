import pytest
from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.email_generators.generator import generate_email, generate_email_event, get_event_ical


def test_generate_email():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    u = users.add("test@test.com", 'name', 'alias', 'psw', 8)
    html = generate_email('test', 'usertest.html', root='./src/', user=u)
    assert html
    assert type(html) == str


def test_generate_email_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    u = users.add("test@test.com", 'name', 'alias', 'psw', 8)
    e = events.add('test', 'test', 30, start, dur, 'test', 'test',
                   'test@test.com', 'test', u)
    event_obj = generate_email_event(e)
    assert 'day' in event_obj
    assert 'start' in event_obj
    assert 'times' in event_obj
    assert 'description' in event_obj
    assert 'location' in event_obj
    assert 'organizer_name' in event_obj

def test_get_event_ical():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    u = users.add("test@test.com", 'name', 'alias', 'psw', 8)
    e = events.add('test', 'test', 30, start, dur, 'test', 'test',
                   'test@test.com', 'test', u)
    ical = get_event_ical(e)
    assert ical
    assert type(ical) == str
