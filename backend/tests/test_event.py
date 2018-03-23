from datetime import datetime, timedelta
import pytz
from src.event import Event


def test_event():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = Event("test", "test", start, dur, 'test', 'test', 'test@test.com', 'test')
    assert e.uid == "test"
    assert e.title == "test"
    assert e.description == "test"
    assert e.start == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.duration == dur.total_seconds()
    assert e.end == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.location == "test"
    assert e.organizer_name == "test"
    assert e.organizer_email == "test@test.com"
    uid = e.generate_uid()
    assert uid
    assert type(uid) == str


def test_default_event():

    e = Event("test", "test")
    start = datetime.strptime(e.start, "%Y-%m-%dT%H:%M:%SZ")
    dur = timedelta(seconds=e.duration)
    end = start + dur
    assert e.title == "test"
    assert e.description == "test"
    assert e.start == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.duration == dur.total_seconds()
    assert e.end == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.location == ""
    assert e.organizer_name == ""
    assert e.organizer_email == ""
    assert e.uid
    assert type(e.uid) == str
