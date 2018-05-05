from src.access import UserUpdateAccess
from generate_access_data import generate_access_data


def test_update_user_access():
    sessions = generate_access_data()
    user = sessions['user'].users.get('user')
    useraccess = UserUpdateAccess(sessions['user'], user)
    manageraccess = UserUpdateAccess(sessions['manager'], user)
    superaccess = UserUpdateAccess(sessions['super'], user)
    noneaccess = UserUpdateAccess(sessions['none'], user)
    assert useraccess.granted()
    assert not manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
