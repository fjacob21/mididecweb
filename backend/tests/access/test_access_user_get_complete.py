from src.access import UserGetCompleteAccess
from generate_access_data import generate_access_data


def test_get_complete_user_access():
    sessions = generate_access_data()
    user = sessions['user'].users.get('user')
    useraccess = UserGetCompleteAccess(sessions['user'], user)
    manageraccess = UserGetCompleteAccess(sessions['manager'], user)
    superaccess = UserGetCompleteAccess(sessions['super'], user)
    noneaccess = UserGetCompleteAccess(sessions['none'], user)
    assert useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()


def test_get_complete_user_access_not_owning_user():
    sessions = generate_access_data()
    user = sessions['user'].users.get('super')
    useraccess = UserGetCompleteAccess(sessions['user'], user)
    manageraccess = UserGetCompleteAccess(sessions['manager'], user)
    superaccess = UserGetCompleteAccess(sessions['super'], user)
    noneaccess = UserGetCompleteAccess(sessions['none'], user)
    assert not useraccess.granted()
    assert not manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()


def test_get_complete_user_access_is_user():
    sessions = generate_access_data()
    attendee = sessions['user'].users.get('super')
    user = sessions['user'].users.get('user')
    useraccess = UserGetCompleteAccess(sessions['user'], user)
    manageraccess = UserGetCompleteAccess(sessions['manager'], attendee)
    superaccess = UserGetCompleteAccess(sessions['super'], attendee)
    noneaccess = UserGetCompleteAccess(sessions['none'], user)
    assert useraccess.granted()
    assert not manageraccess.granted()
    assert superaccess.granted()
    assert not noneaccess.granted()
