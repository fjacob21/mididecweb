from src.codec.users_json_encoder import UsersJsonEncoder
from src.users import Users
from src.user import USER_ACCESS_SUPER
from src.stores import MemoryStore
import json


def generate_user(users):
    return users.add('test@test.com', 'name', 'alias', 'psw', '1234567890',
                     True, True, 'profile', USER_ACCESS_SUPER, True, False,
                     'test')


def test_complete_users_json_encoder():
    store = MemoryStore()
    users = Users(store)
    generate_user(users)
    jsonobj = UsersJsonEncoder(users, True).encode('dict')
    assert jsonobj['count'] == 1
    assert len(jsonobj['users']) == 1


def test_complete_users_json_encoder_string():
    store = MemoryStore()
    users = Users(store)
    generate_user(users)
    jsonstr = UsersJsonEncoder(users, True).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['count'] == 1
    assert len(jsonobj['users']) == 1
