from src.access import EventRemoveAccess
from generate_access_data import generate_access_data


def test_remove_event_access():
    sessions = generate_access_data()
    event = sessions['user'].events.get('test')
    useraccess = EventRemoveAccess(sessions['user'], event)
    manageraccess = EventRemoveAccess(sessions['manager'], event)
    superaccess = EventRemoveAccess(sessions['super'], event)
    noneaccess = EventRemoveAccess(sessions['none'], event)
    assert not useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
