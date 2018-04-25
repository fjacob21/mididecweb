from datetime import datetime, timedelta
import pytz
from src.event import Event, WAITING_LIST, ATTENDEE_LIST, ALREADY_ATTENDEE_LIST
from src.events import Events
from src.attendee import Attendee
from src.stores import MemoryStore


def test_event():
    store = MemoryStore()
    events = Events(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    e = events.add('test', 'test', 30, start, dur, 'test', 'test',
                   'test@test.com', 'test')
    assert e.event_id == "test"
    assert e.title == "test"
    assert e.description == "test"
    assert e.max_attendee == 30
    assert e.start == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.duration == dur.total_seconds()
    assert e.end == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.location == "test"
    assert e.organizer_name == "test"
    assert e.organizer_email == "test@test.com"


def test_default_event():
    store = MemoryStore()
    events = Events(store)
    e = events.add("test", "test")
    start = datetime.strptime(e.start, "%Y-%m-%dT%H:%M:%SZ")
    dur = timedelta(seconds=e.duration)
    end = start + dur
    assert e.title == "test"
    assert e.description == "test"
    assert e.max_attendee == 20
    assert e.start == start.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.duration == dur.total_seconds()
    assert e.end == end.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert e.location == ""
    assert e.organizer_name == ""
    assert e.organizer_email == ""
    assert e.event_id
    assert type(e.event_id) == str


# def test_register_attendee():
#     e = Event("test", "test")
#     a = Attendee("test", "test@test.com", '1234567890', True, True)
#     res = e.register_attendee(a)
#     assert len(e.attendees) == 1
#     assert e.attendees[0] == a
#     assert res == ATTENDEE_LIST
#
#
# def test_double_register_attendee():
#     e = Event("test", "test")
#     a = Attendee("test", "test@test.com", '1234567890', True, True)
#     res1 = e.register_attendee(a)
#     res2 = e.register_attendee(a)
#     assert len(e.attendees) == 1
#     assert e.attendees[0] == a
#     assert res1 == ATTENDEE_LIST
#     assert res2 == ALREADY_ATTENDEE_LIST
#
#
# def test_max_attendee():
#     e = Event("test", "test", max_attendee=1)
#     a1 = Attendee("test", "test@test.com", '1234567890', True, True)
#     a2 = Attendee("test2", "test2@test.com", '1234567898', True, True)
#     res1 = e.register_attendee(a1)
#     res2 = e.register_attendee(a2)
#     assert len(e.attendees) == 1
#     assert e.attendees[0] == a1
#     assert res1 == ATTENDEE_LIST
#     assert len(e.waiting_attendees) == 1
#     assert e.waiting_attendees[0] == a2
#     assert res2 == WAITING_LIST
#
#
# def test_cancel_register():
#     e = Event("test", "test", max_attendee=1)
#     a1 = Attendee("test", "test@test.com", '1234567890', True, True)
#     a2 = Attendee("test2", "test2@test.com", '1234567898', True, True)
#     res1 = e.register_attendee(a1)
#     res2 = e.register_attendee(a2)
#     assert len(e.attendees) == 1
#     assert e.attendees[0] == a1
#     assert res1 == ATTENDEE_LIST
#     assert len(e.waiting_attendees) == 1
#     assert e.waiting_attendees[0] == a2
#     assert res2 == WAITING_LIST
#     e.cancel_registration(a1.email)
#     assert len(e.attendees) == 1
#     assert len(e.waiting_attendees) == 0
#     assert e.attendees[0] == a2
#     e.cancel_registration(a2.email)
#     assert len(e.attendees) == 0
#     assert len(e.waiting_attendees) == 0
#     res1 = e.register_attendee(a1)
#     res2 = e.register_attendee(a2)
#     e.cancel_registration(a2.email)
#     assert len(e.attendees) == 1
#     assert len(e.waiting_attendees) == 0
