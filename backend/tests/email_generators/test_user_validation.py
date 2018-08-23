import pytest
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
from src.events import Events
from src.users import Users
from src.user import USER_ACCESS_MANAGER
from src.stores import MemoryStore
from src.email_generators import UserValidationEmail


def test_user_validation_email():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    end = start + dur
    u = users.add("test@test.com", 'name', 'alias', 'psw', 8)
    e = events.add('test', 'test', 30, start, dur, 'test', 'test',
                   'test@test.com', 'test', u)
    email = UserValidationEmail('', root='./src')
    html = email.generate(u)
    soup = BeautifulSoup(html, 'html.parser')
    assert html
    assert type(html) == str
    assert bool(soup.find())
