from src.attendee import Attendee
from datetime import datetime, timedelta
import pytz
import pytest
from src.event import WAITING_LIST, ATTENDEE_LIST, ALREADY_ATTENDEE_LIST
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_NORMAL
from src.stores import MemoryStore


def test_attendee():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890', True,
                  True, 'profile', USER_ACCESS_NORMAL, True, False, 'test')
    e = events.add('test', 'test', 30, start, dur, 'test', 'test',
                   'test@test.com', 'test', u)
    e.register_attendee(u)
    a = Attendee(store, u.user_id, e.event_id)
    assert a.user_id == 'test'
    assert a.email == 'test@test.com'
    assert a.name == 'name'
    assert a.alias == 'alias'
    assert a.phone == '1234567890'
    assert a.useemail
    assert a.usesms
    assert a.profile == 'profile'
    assert a.access == USER_ACCESS_NORMAL
    assert a.validated
    assert not a.smsvalidated
    assert a.lastlogin == ''
    assert a.loginkey == ''
    assert not a.present
    assert a.present_time == ''
