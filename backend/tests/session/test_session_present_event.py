from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.event import ATTENDEE_LIST, ALREADY_ATTENDEE_LIST
from src.event import WAITING_LIST, ALREADY_WAITING_LIST
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.session import Session


def test_present_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     access=USER_ACCESS_MANAGER, user_id='userid')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    event = events.add('test', 'test', 30, start, dur, 'test', 'test',
                       'test@test.com', 'eventid', owner=user)
    event.register_attendee(user)

    params = {}
    params['user_id'] = 'userid'
    params['present'] = True

    session = Session(params, store, 'userid')
    result_dict = session.present_event('eventid')
    assert result_dict
    assert result_dict['result']

def test_present_event_bad_user():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     access=USER_ACCESS_MANAGER, user_id='userid')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    event = events.add('test', 'test', 30, start, dur, 'test', 'test',
                       'test@test.com', 'eventid', owner=user)
    event.register_attendee(user)

    params = {}
    params['user_id'] = ''
    params['present'] = True

    session = Session(params, store, 'userid')
    with pytest.raises(Exception):
        result_dict = session.present_event('eventid')
