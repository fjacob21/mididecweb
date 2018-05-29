from datetime import datetime, timedelta
import pytz
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_NORMAL, USER_ACCESS_MANAGER, USER_ACCESS_SUPER
from src.stores import MemoryStore
from src.session import Session


def generate_access_data():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)

    add_general_user(users)
    add_manager_user(users)
    add_super_user(users)
    owner = users.get('manager')
    user = users.get('user')
    add_event(events, owner, user)
    usersession = Session({}, store, 'user')
    managersession = Session({}, store, 'manager')
    supersession = Session({}, store, 'super')
    nonesession = Session({}, store, '')
    sessions = {}
    sessions['user'] = usersession
    sessions['manager'] = managersession
    sessions['super'] = supersession
    sessions['none'] = nonesession
    return sessions


def add_event(events, owner, attendee):
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    e = events.add('test', 'test', 20, start, dur, 'test', 'test',
                   'manageremail', 'test', owner)
    e.register_attendee(attendee)


def add_general_user(users):
    user = users.add('useremail', 'user', 'alias', 'psw', 'phone', True, True,
                     access=USER_ACCESS_NORMAL, user_id='user')
    user.validated = True


def add_manager_user(users):
    user = users.add('manageremail', 'manager', 'alias', 'psw', 'phone', True, True,
                     access=USER_ACCESS_MANAGER, user_id='manager')
    user.validated = True


def add_super_user(users):
    user = users.add('superemail', 'super', 'alias', 'psw', 'phone', True, True,
                     access=USER_ACCESS_SUPER, user_id='super')
    user.validated = True
