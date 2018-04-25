from datetime import datetime, timedelta
import pytz
from icalendar import Calendar
from src.events import Events
from src.icalgenerator import iCalGenerator
from src.stores import MemoryStore


def generate_event(events):
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return events.add("test", "test", 20, start, dur, 'test', 'test', 'test@test.com', 'test')


def test_generate_ical():
    store = MemoryStore()
    events = Events(store)
    e = generate_event(events)
    gen = iCalGenerator(e)
    ical = gen.generate()
    assert ical
    assert type(ical) == str
    cal = Calendar.from_ical(ical)
    assert cal.to_ical().decode() == ical
    assert cal.get('DTSTART').dt.strftime("%Y-%m-%dT%H:%M:%SZ") == e.start
    ev = cal.subcomponents[0]
    assert ev.get('DTSTART').dt.strftime("%Y-%m-%dT%H:%M:%SZ") == e.start
    assert ev.get('DTEND').dt.strftime("%Y-%m-%dT%H:%M:%SZ") == e.end
