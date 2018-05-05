from src.access import UserAddAccess
from generate_access_data import generate_access_data


def test_add_user_access():
    sessions = generate_access_data()
    useraccess = UserAddAccess(sessions['user'])
    manageraccess = UserAddAccess(sessions['manager'])
    superaccess = UserAddAccess(sessions['super'])
    noneaccess = UserAddAccess(sessions['none'])
    assert useraccess.granted()
    assert manageraccess.granted()
    assert superaccess.granted()
    assert noneaccess.granted()
