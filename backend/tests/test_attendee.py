from src.attendee import Attendee


def test_attendee():
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    assert a.name == "test"
    assert a.email == "test@test.com"
    assert a.phone == "1234567890"
    assert a.sendremindemail is True
    assert a.sendremindsms is True
