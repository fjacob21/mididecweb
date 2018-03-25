from src.mailinglist_member import MailingListMember
from src.mailinglist import MailingList


def test_mailinglist_add():
    ml = MailingList()
    m = MailingListMember("test", "test@test.com", '1234567890', False, True)
    ml.register(m)
    assert len(ml.members) == 1
    assert ml.members[0] == m


def test_mailinglist_remove():
    ml = MailingList()
    m = MailingListMember("test", "test@test.com", '1234567890', False, True)
    ml.register(m)
    assert len(ml.members) == 1
    assert ml.members[0] == m
    ml.unregister(m.email)
    assert len(ml.members) == 0
    ml.unregister(m.email)


def test_mailinglist_find():
    ml = MailingList()
    m = MailingListMember("test", "test@test.com", '1234567890', False, True)
    assert ml.find_member(m.email) == -1
    ml.register(m)
    assert ml.find_member(m.email) == 0
