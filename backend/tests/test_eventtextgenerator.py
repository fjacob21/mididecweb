from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.eventtextgenerator import EventTextGenerator
from src.stores import MemoryStore


def generate_event(events):

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return events.add("test", "test", 20, start, dur, 'test', 'test', 'fjacob21@hotmail.com', 'test')


def test_generate_event_text_short():
    store = MemoryStore()
    events = Events(store)
    e = generate_event(events)
    gen = EventTextGenerator(e)
    text = gen.generate()
    assert text
    assert type(text) == str


def test_generate_event_text_long():
    store = MemoryStore()
    events = Events(store)
    e = generate_event(events)
    gen = EventTextGenerator(e, False)
    text = gen.generate()
    assert text
    assert type(text) == str
