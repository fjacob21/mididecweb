from src.codec.events_json_encoder import EventsJsonEncoder
from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.stores import MemoryStore
import json


def generate_event(events):
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return events.add("test", "test", 20, start, dur, 'test', 'test', 'test@test.com', 'test')


def test_complete_events_json_encoder():
    store = MemoryStore()
    events = Events(store)
    generate_event(events)
    jsonobj = EventsJsonEncoder(events, True).encode('dict')
    assert jsonobj['count'] == 1
    assert len(jsonobj['events']) == 1


def test_complete_events_json_encoder_string():
    store = MemoryStore()
    events = Events(store)
    generate_event(events)
    jsonstr = EventsJsonEncoder(events, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['count'] == 1
    assert len(jsonobj['events']) == 1
