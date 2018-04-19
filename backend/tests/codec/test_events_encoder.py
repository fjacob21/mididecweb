from src.codec.events_json_encoder import EventsJsonEncoder
from datetime import datetime, timedelta
import pytz
from src.event import Event
from src.events import Events
import json


def generate_event():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    return Event("test", "test", 20, start, dur, 'test', 'test', 'test@test.com', 'test')


def test_complete_events_json_encoder():
    e = generate_event()
    events = Events()
    events.add(e)
    jsonobj = EventsJsonEncoder(events, True).encode('dict')
    assert jsonobj['count'] == 1
    assert len(jsonobj['events']) == 1


def test_complete_events_json_encoder_string():
    e = generate_event()
    events = Events()
    events.add(e)
    jsonstr = EventsJsonEncoder(events, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['count'] == 1
    assert len(jsonobj['events']) == 1
