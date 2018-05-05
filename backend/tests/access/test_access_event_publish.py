from src.access import EventPublishAccess
from generate_access_data import generate_access_data


def test_publish_event_access():
    sessions = generate_access_data()
    event = sessions['user'].events.get('test')
    useraccess = EventPublishAccess(sessions['user'], event)
    manageraccess = EventPublishAccess(sessions['manager'], event)
    superaccess = EventPublishAccess(sessions['super'], event)
    noneaccess = EventPublishAccess(sessions['none'], event)
    assert not useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
