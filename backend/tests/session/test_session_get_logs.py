from src.logs import Logs
from src.users import Users
from src.user import USER_ACCESS_SUPER
from src.stores import MemoryStore
from src.session import Session


def test_get_logs():
    store = MemoryStore()
    logs = Logs(store)
    users = Users(store)
    user = users.add('email', 'name', 'alias', 'password', 'phone', True, True,
                     access=USER_ACCESS_SUPER, user_id='test')
    user.validated = True
    session = Session({}, store, 'test')

    log = logs.add("ip", "os", "os_version", "browser", "browser_version", 'continent', False, 'country', 'country_emoji', 'region', 'city')
    logs_dict = session.get_logs()
    assert logs_dict
    assert 'logs' in logs_dict
    assert 'logs' in logs_dict['logs']
    assert 'count' in logs_dict['logs']
    assert logs_dict['logs']['count'] == 1
    assert len(logs_dict['logs']['logs']) == 1
