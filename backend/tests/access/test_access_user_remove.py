from src.access import UserRemoveAccess
from generate_access_data import generate_access_data


def test_remove_user_access():
    sessions = generate_access_data()
    user = sessions['user'].users.get('user')
    useraccess = UserRemoveAccess(sessions['user'], user)
    manageraccess = UserRemoveAccess(sessions['manager'], user)
    superaccess = UserRemoveAccess(sessions['super'], user)
    noneaccess = UserRemoveAccess(sessions['none'], user)
    assert useraccess.granted()
    assert not manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
