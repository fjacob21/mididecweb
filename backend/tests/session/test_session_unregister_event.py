from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_unregister_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    event = events.add('test', 'test', 30, start, dur, 'test', 'test',
                       'test@test.com', 'test')
    user = users.add('email', 'name', 'name', 'psw', 'phone', True, True)
    user.validated = True
    loginkey = user.login('psw')
    event.register_attendee(user)
    params = {}
    params['loginkey'] = loginkey

    session = Session(params, events, users, '')
    result_dict = session.unregister_event('')
    assert not result_dict
    assert len(event.attendees) == 1
    result_dict = session.unregister_event('test')
    assert result_dict
    assert len(event.attendees) == 0
    result_dict = session.unregister_event('test')
    assert not result_dict
    assert len(event.attendees) == 0


def test_unregister_event_bad_email():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    event = events.add('test', 'test', 30, start, dur, 'test', 'test',
                       'test@test.com', 'test')
    user = users.add('email', 'name', 'name', '', 'phone', True, True)
    event.register_attendee(user)
    params = {}
    params['email'] = 'bademail'

    session = Session(params, events, users, '')
    result_dict = session.unregister_event('test')
    assert not result_dict
    assert len(event.attendees) == 1
