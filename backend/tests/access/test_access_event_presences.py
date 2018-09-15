from src.access import EventPresencesAccess
from generate_access_data import generate_access_data


def test_presences_event_access():
    sessions = generate_access_data()
    event = sessions['user'].events.get('test')
    useraccess = EventPresencesAccess(sessions['user'], event)
    manageraccess = EventPresencesAccess(sessions['manager'], event)
    superaccess = EventPresencesAccess(sessions['super'], event)
    noneaccess = EventPresencesAccess(sessions['none'], event)
    assert not useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
