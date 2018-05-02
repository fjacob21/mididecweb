from src.mailinglist import MailingList
from src.users import Users
from src.stores import MemoryStore


def test_mailinglist_add():
    store = MemoryStore()
    ml = MailingList(store)
    users = Users(store)
    m = users.add("test@test.com", 'name', 'alias', 'psw')
    ml.register(m)
    assert len(ml.members) == 1
    assert ml.members[0] == m


def test_mailinglist_remove():
    store = MemoryStore()
    ml = MailingList(store)
    users = Users(store)
    m = users.add("test@test.com", 'name', 'alias', 'psw')
    ml.register(m)
    assert len(ml.members) == 1
    assert ml.members[0] == m
    ml.unregister(m.email)
    assert len(ml.members) == 0
    ml.unregister(m.email)


def test_mailinglist_find():
    store = MemoryStore()
    ml = MailingList(store)
    users = Users(store)
    m = users.add("test@test.com", 'name', 'alias', 'psw')
    assert ml.find_member(m.email) == -1
    ml.register(m)
    assert ml.find_member(m.email) == 0
