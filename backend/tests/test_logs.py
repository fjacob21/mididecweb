from datetime import datetime
import pytz
from src.stores import MemoryStore
from src.logs import Logs


def generate_log(logs, is_eu=False):
    l = logs.add('0.0.0.0', 'os', '1.0.0', 'browser', '1.0.0', 'continent',
                 is_eu, 'country', 'country_emoji', 'region', 'city')
    return l


def test_generate_uid():
    start = datetime.now(pytz.timezone("America/New_York"))
    store = MemoryStore()
    logs = Logs(store)
    uid = logs.generate_log_id('0.0.0.0', start)
    assert uid
    assert type(uid) == str


def test_add_event():
    store = MemoryStore()
    logs = Logs(store)
    l = generate_log(logs)
    assert l
    assert logs.count == 1
    assert logs.list[0] == l
