from src.mailinglist_member import MailingListMember


def test_mailinglist_member():
    m = MailingListMember("test", "test@test.com", '1234567890', False, True)
    assert m.name == "test"
    assert m.email == "test@test.com"
    assert m.phone == "1234567890"
    assert m.useemail is False
    assert m.usesms is True


def test_default_mailinglist_member():
    m = MailingListMember("test", "test@test.com", '1234567890')
    assert m.name == "test"
    assert m.email == "test@test.com"
    assert m.phone == "1234567890"
    assert m.useemail is True
    assert m.usesms is False
