from src.access import EventRegisterAccess
from generate_access_data import generate_access_data


def test_register_event_access():
    sessions = generate_access_data()
    event = sessions['user'].events.get('test')
    useraccess = EventRegisterAccess(sessions['user'], event)
    manageraccess = EventRegisterAccess(sessions['manager'], event)
    superaccess = EventRegisterAccess(sessions['super'], event)
    noneaccess = EventRegisterAccess(sessions['none'], event)
    assert useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
