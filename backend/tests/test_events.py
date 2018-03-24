from datetime import datetime, timedelta
import pytz
from src.event import Event
from src.events import Events


def generate_event():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return Event("test", "test", 20, start, dur, 'test', 'test', 'test@test.com', 'test')


def test_add_event():
    e = generate_event()
    events = Events()

    events.add(e)
    assert events.count == 1
    assert events.list[0] == e
    ge = events.get('test')
    assert ge
    assert ge == e
    ge = events.get('test2')
    assert not ge
    assert events.index('test') == 0
    assert events.index('test2') == -1


def test_remove_event():
    e = generate_event()
    events = Events()

    events.add(e)
    events.remove(e.uid)
    assert events.count == 0
    ge = events.get('test')
    assert not ge
    assert events.index('test') == -1
