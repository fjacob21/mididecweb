from src.access import EventAddAccess
from generate_access_data import generate_access_data


def test_add_event_access():
    sessions = generate_access_data()
    useraccess = EventAddAccess(sessions['user'])
    manageraccess = EventAddAccess(sessions['manager'])
    superaccess = EventAddAccess(sessions['super'])
    noneaccess = EventAddAccess(sessions['none'])
    assert not useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
