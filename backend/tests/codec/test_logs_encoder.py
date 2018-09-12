from src.codec.logs_json_encoder import LogsJsonEncoder
from src.logs import Logs
from src.stores import MemoryStore


def generate_log(logs):
    return logs.add("ip", "os", "os_version", "browser", "browser_version", 'continent', False, 'country', 'country_emoji', 'region', 'city')


def test_complete_events_json_encoder():
    store = MemoryStore()
    logs = Logs(store)
    generate_log(logs)
    jsonobj = LogsJsonEncoder(logs).encode('dict')
    assert jsonobj['count'] == 1
    assert len(jsonobj['logs']) == 1
