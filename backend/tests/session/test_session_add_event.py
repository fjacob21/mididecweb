from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.session import Session


def test_add_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    users.add('email', 'name', 'alias', 'password', 'phone', True, True,
              access=USER_ACCESS_MANAGER, user_id='test')
    params = {}
    params['title'] = 'title'
    params['desc'] = 'desc'
    params['max_attendee'] = 1
    params['start'] = '2018-04-26T13:00:00Z'
    params['duration'] = 3600
    params['location'] = 'location'
    params['organizer_name'] = 'organizer_name'
    params['organizer_email'] = 'organizer_email'
    params['event_id'] = 'event_id'
    session = Session(params, events, users, 'test')

    event_dict = session.add_event()
    assert event_dict
    assert 'event' in event_dict
    assert len(events.list) == 1


def test_add_event_bad_title():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['desc'] = 'desc'
    params['max_attendee'] = 1
    params['start'] = '2018-04-26T13:00:00Z'
    params['duration'] = 3600
    params['location'] = 'location'
    params['organizer_name'] = 'organizer_name'
    params['organizer_email'] = 'organizer_email'
    params['event_id'] = 'event_id'
    session = Session(params, events, users, '')

    event_dict = session.add_event()
    assert not event_dict
    assert len(events.list) == 0


def test_add_event_bad_desc():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    params = {}
    params['title'] = 'title'
    params['max_attendee'] = 1
    params['start'] = '2018-04-26T13:00:00Z'
    params['duration'] = 3600
    params['location'] = 'location'
    params['organizer_name'] = 'organizer_name'
    params['organizer_email'] = 'organizer_email'
    params['event_id'] = 'event_id'
    session = Session(params, events, users, '')

    event_dict = session.add_event()
    assert not event_dict
    assert len(events.list) == 0


def test_double_add_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    users.add('email', 'name', 'alias', 'password', 'phone', True, True,
              access=USER_ACCESS_MANAGER, user_id='test')
    params = {}
    params['title'] = 'title'
    params['desc'] = 'desc'
    params['max_attendee'] = 1
    params['start'] = '2018-04-26T13:00:00Z'
    params['duration'] = 3600
    params['location'] = 'location'
    params['organizer_name'] = 'organizer_name'
    params['organizer_email'] = 'organizer_email'
    params['event_id'] = 'event_id'
    session = Session(params, events, users, 'test')

    event_dict = session.add_event()
    assert event_dict
    assert 'event' in event_dict
    assert len(events.list) == 1
    event_dict2 = session.add_event()
    assert event_dict2
    assert 'event' in event_dict2
    assert len(events.list) == 1
    assert event_dict == event_dict2
