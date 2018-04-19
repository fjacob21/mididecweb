from src.codec.event_json_encoder import EventJsonEncoder
from datetime import datetime, timedelta
import pytz
from src.event import Event
from src.attendee import Attendee
import json


def test_complete_event_json_encoder():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonobj = EventJsonEncoder(e, True).encode('dict')
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert jsonobj['organizer_email'] == "test@test.com"
    assert len(jsonobj['attendees']) == 1


def test_event_json_encoder():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonobj = EventJsonEncoder(e).encode('dict')
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert 'organizer_email' not in jsonobj
    assert len(jsonobj['attendees']) == 1


def test_event_no_attendees_json_encoder():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonobj = EventJsonEncoder(e, show_attendee=False).encode('dict')
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert 'organizer_email' not in jsonobj
    assert 'attendees' not in jsonobj


def test_complete_event_json_encoder_string():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonstr = EventJsonEncoder(e, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert jsonobj['organizer_email'] == "test@test.com"
    assert len(jsonobj['attendees']) == 1


def test_event_json_encoder_string():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonstr = EventJsonEncoder(e).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert 'organizer_email' not in jsonobj
    assert len(jsonobj['attendees']) == 1


def test_event_no_attendees_json_encoder_string():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test')
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    e.register_attendee(a)
    jsonstr = EventJsonEncoder(e, show_attendee=False).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['uid'] == "test"
    assert jsonobj['title'] == "test"
    assert jsonobj['description'] == "test"
    assert jsonobj['max_attendee'] == 30
    assert jsonobj['start'] == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['duration'] == dur.total_seconds()
    assert jsonobj['end'] == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert jsonobj['location'] == "test"
    assert jsonobj['organizer_name'] == "test"
    assert 'organizer_email' not in jsonobj
    assert 'attendees' not in jsonobj
