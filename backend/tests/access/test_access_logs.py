from src.access import LogsAccess
from generate_access_data import generate_access_data


def test_logs_access():
    sessions = generate_access_data()
    useraccess = LogsAccess(sessions['user'])
    manageraccess = LogsAccess(sessions['manager'])
    superaccess = LogsAccess(sessions['super'])
    noneaccess = LogsAccess(sessions['none'])
    assert not useraccess.granted()
    assert not manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
