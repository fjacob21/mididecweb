from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.event import ATTENDEE_LIST, ALREADY_ATTENDEE_LIST
from src.event import WAITING_LIST, ALREADY_WAITING_LIST
from src.users import Users
from src.user import USER_ACCESS_NORMAL
from src.stores import MemoryStore
from src.session import Session


def test_register_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    users.add('email', 'name', 'alias', 'password', 'phone', True, True,
              access=USER_ACCESS_NORMAL, user_id='test')
    params = {}
    params['name'] = 'name'
    params['email'] = 'email'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True

    session = Session(params, events, users, 'test')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    result_dict = session.register_event('')
    assert not result_dict
    result_dict = session.register_event('test')
    assert result_dict
    assert result_dict['result'] == ATTENDEE_LIST
    event = events.get('test')
    assert len(event.attendees) == 1
    result_dict = session.register_event('test')
    assert result_dict
    assert result_dict['result'] == ALREADY_ATTENDEE_LIST
    event = events.get('test')
    assert len(event.attendees) == 1


def test_register_event_bad_name():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)

    params = {}
    params['email'] = 'email'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True

    session = Session(params, events, users, '')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events = events.add('test', 'test', 30, start, dur, 'test', 'test',
                        'test@test.com', 'test')
    result_dict = session.register_event('test')
    assert not result_dict


def test_register_event_bad_email():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)

    params = {}
    params['name'] = 'name'
    params['phone'] = 'phone'
    params['useemail'] = True
    params['usesms'] = True

    session = Session(params, events, users, '')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events = events.add('test', 'test', 30, start, dur, 'test', 'test',
                        'test@test.com', 'test')
    result_dict = session.register_event('test')
    assert not result_dict


def test_register_event_waiting():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     access=USER_ACCESS_NORMAL, user_id='test')
    loginkey = user.login('password')
    params = {}
    params['loginkey'] = loginkey

    session = Session(params, events, users, 'test')

    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 1, start, dur, 'test', 'test',
               'test@test.com', 'test')
    result_dict = session.register_event('test')
    assert result_dict
    event = events.get('test')
    assert len(event.attendees) == 1

    user2 = users.add('email2', 'name2', 'alias2', 'password', 'phone', True,
                      True, access=USER_ACCESS_NORMAL, user_id='test2')
    loginkey2 = user2.login('password')
    params = {}
    params['loginkey'] = loginkey2

    session = Session(params, events, users, 'test')
    result_dict = session.register_event('test')
    assert result_dict
    assert result_dict['result'] == WAITING_LIST
    event = events.get('test')
    assert len(event.attendees) == 1
    assert len(event.waiting_attendees) == 1
    result_dict = session.register_event('test')
    assert result_dict
    assert result_dict['result'] == ALREADY_WAITING_LIST
    event = events.get('test')
    assert len(event.attendees) == 1
    assert len(event.waiting_attendees) == 1
