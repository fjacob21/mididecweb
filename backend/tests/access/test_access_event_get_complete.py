from src.access import EventGetCompleteAccess
from generate_access_data import generate_access_data


def test_get_complete_event_access():
    sessions = generate_access_data()
    event = sessions['user'].events.get('test')
    useraccess = EventGetCompleteAccess(sessions['user'], event)
    manageraccess = EventGetCompleteAccess(sessions['manager'], event)
    superaccess = EventGetCompleteAccess(sessions['super'], event)
    noneaccess = EventGetCompleteAccess(sessions['none'], event)
    assert not useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
