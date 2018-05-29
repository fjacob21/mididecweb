from datetime import datetime, timedelta
import pytz
import pytest
from src.events import Events
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_publish_event():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    users.add('email', 'name', 'name', '', 'phone', True, True)
    params = {}
    params['usr'] = 'usr'
    params['psw'] = 'psw'
    params['sid'] = 'sid'
    params['token'] = 'token'

    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.publish_event('')
    with pytest.raises(Exception):
        session.publish_event('test')


def test_publish_event_missing_usr():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    users.add('email', 'name', 'name', '', 'phone', True, True)
    params = {}
    params['psw'] = 'psw'
    params['sid'] = 'sid'
    params['token'] = 'token'

    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.publish_event('test')


def test_publish_event_missing_psw():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    users.add('email', 'name', 'name', '', 'phone', True, True)
    params = {}
    params['usr'] = 'usr'
    params['sid'] = 'sid'
    params['token'] = 'token'

    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.publish_event('test')


def test_publish_event_missing_sid():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    users.add('email', 'name', 'name', '', 'phone', True, True)
    params = {}
    params['usr'] = 'usr'
    params['psw'] = 'psw'
    params['token'] = 'token'

    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.publish_event('test')


def test_publish_event_missing_token():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    events.add('test', 'test', 30, start, dur, 'test', 'test',
               'test@test.com', 'test')
    users.add('email', 'name', 'name', '', 'phone', True, True)
    params = {}
    params['usr'] = 'usr'
    params['psw'] = 'psw'
    params['sid'] = 'sid'

    session = Session(params, store, '')
    with pytest.raises(Exception):
        session.publish_event('test')
