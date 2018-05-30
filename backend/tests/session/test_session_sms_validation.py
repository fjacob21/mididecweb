from bcrypt_hash import BcryptHash
import pytest
from src.users import Users
from src.stores import MemoryStore
from src.session import Session


def test_sms_validation():
    store = MemoryStore()
    users = Users(store)
    password = BcryptHash('password').encrypt()
    user = users.add('email', 'name', 'alias', password, '5551255478', True,
                     True, user_id='test')
    user.validated = True
    session = Session({}, store, 'test')

    with pytest.raises(Exception):
        session.sendcode('')
    result_dict = session.sendcode('test')
    assert result_dict
    assert 'result' in result_dict
    assert result_dict['result']
    assert user.smscode
    code = user.smscode
    params = {}
    params['smscode'] = code
    session = Session(params, store, 'test')

    with pytest.raises(Exception):
        session.validatecode('')
    result_dict = session.validatecode('test')
    assert result_dict
    assert 'result' in result_dict
    assert result_dict['result']
