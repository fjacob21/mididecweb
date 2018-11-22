from src.codec.attendee_json_encoder import AttendeeJsonEncoder
from src.attendee import Attendee
from datetime import datetime, timedelta
import pytz
from src.events import Events
import json
from src.stores import MemoryStore
from src.users import Users
from src.user import USER_ACCESS_SUPER


def test_complete_attendee_json_encoder():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    u = users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                  True, True, 'profile', USER_ACCESS_SUPER, True, False,
                  'test')
    e = events.add("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test', u)
    e.register_attendee(u)
    a = Attendee(store, u.user_id, e.event_id)
    jsonobj = AttendeeJsonEncoder(a).encode('dict')
    assert jsonobj['user_id'] == "test"
    assert jsonobj['name'] == "name"
    assert jsonobj['alias'] == "alias"
    assert jsonobj['email'] == "test@test.com"
    assert jsonobj['phone'] == '1234567890'
    assert jsonobj['useemail']
    assert jsonobj['usesms']
    assert jsonobj['profile'] == 'profile'
    assert jsonobj['access'] == USER_ACCESS_SUPER
    assert jsonobj['validated']
    assert not jsonobj['smsvalidated']
    assert jsonobj['lastlogin'] == ''
    assert jsonobj['loginkey'] == ''
    assert not jsonobj['present']
    assert jsonobj['present_time'] == ''
    assert 'create_date' in jsonobj
