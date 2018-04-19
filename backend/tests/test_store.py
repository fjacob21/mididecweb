from src.store import Store
from src.event import Event
from src.events import Events
from src.attendee import Attendee
from src.mailinglist import MailingList
from src.mailinglist_member import MailingListMember
from datetime import datetime, timedelta
import pytz


def generate_event():
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    a1 = Attendee("test", "test@test.com", '1234567890', True, True)
    a2 = Attendee("test2", "test2@test.com", '1234567890', True, True)
    ev = Event("test", "test", 1, start, dur, 'test', 'test', 'test@test.com', 'test')
    ev.register_attendee(a1)
    ev.register_attendee(a2)
    return ev


def generate_mailinglist():
    ml = MailingList()
    a1 = MailingListMember("test", "test@test.com", '1234567890', True, True)
    a2 = MailingListMember("test2", "test2@test.com", '1234567890', True, True)
    ml.register(a1)
    ml.register(a2)
    return ml


def test_store_events():
    s = Store(':memory:')
    e = generate_event()
    events = Events()
    events.add(e)
    s.store_events(events)
    re = s.restore_events()
    assert len(re.list) == 1
    assert re.list[0].uid == e.uid
    assert re.list[0].title == e.title
    assert re.list[0].description == e.description
    assert re.list[0].max_attendee == e.max_attendee
    assert re.list[0].start == e.start
    assert re.list[0].duration == e.duration
    assert re.list[0].location == e.location
    assert re.list[0].organizer_name == e.organizer_name
    assert re.list[0].organizer_email == e.organizer_email
    assert len(re.list[0].attendees) == 1
    assert len(re.list[0].waiting_attendees) == 1
    a1 = e.attendees[0]
    a2 = e.waiting_attendees[0]
    ra1 = re.list[0].attendees[0]
    ra2 = re.list[0].waiting_attendees[0]
    assert a1.name == ra1.name
    assert a2.name == ra2.name
    assert a1.email == ra1.email
    assert a2.email == ra2.email
    assert a1.phone == ra1.phone
    assert a2.phone == ra2.phone
    assert a1.useemail == ra1.useemail
    assert a2.useemail == ra2.useemail
    assert a1.usesms == ra1.usesms
    assert a2.usesms == ra2.usesms


def test_store_mailinglist():
    s = Store(':memory:')
    ml = generate_mailinglist()
    s.store_mailinglist(ml)
    rml = s.restore_mailinglist()
    assert len(rml.members) == 2
    a1 = ml.members[0]
    a2 = ml.members[0]
    ra1 = rml.members[0]
    ra2 = rml.members[0]
    assert a1.name == ra1.name
    assert a2.name == ra2.name
    assert a1.email == ra1.email
    assert a2.email == ra2.email
    assert a1.phone == ra1.phone
    assert a2.phone == ra2.phone
    assert a1.useemail == ra1.useemail
    assert a2.useemail == ra2.useemail
    assert a1.usesms == ra1.usesms
    assert a2.usesms == ra2.usesms
