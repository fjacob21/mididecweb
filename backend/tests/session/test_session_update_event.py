from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.session import Session


def test_update_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     access=USER_ACCESS_MANAGER, user_id='test')
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test', user)
    user.validated = True
    params = {}
    params['title'] = 'title2'
    params['description'] = 'desc2'
    params['max_attendee'] = 2
    params['start'] = '2018-04-26T13:12:00Z'
    params['duration'] = 3601
    params['location'] = 'location2'
    session = Session(params, store, 'test')

    with pytest.raises(Exception):
        session.update_event('')
    event_dict = session.update_event('test')
    assert event_dict
    assert 'event' in event_dict
    assert event_dict['event']['title'] == 'title2'
