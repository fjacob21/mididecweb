from src.codec.log_json_encoder import LogJsonEncoder
from src.logs import Logs
from src.stores import MemoryStore


def test_log_json_encoder():
    store = MemoryStore()
    logs = Logs(store)
    l = logs.add("ip", "os", "os_version", "browser", "browser_version", 'continent', False, 'country', 'country_emoji', 'region', 'city')
    jsonobj = LogJsonEncoder(l).encode('dict')
    assert jsonobj['log_id'] == l.log_id
    assert jsonobj['ip'] == "ip"
    assert jsonobj['os'] == "os"
    assert jsonobj['os_version'] == 'os_version'
    assert jsonobj['browser'] == 'browser'
    assert jsonobj['browser_version'] == 'browser_version'
    assert jsonobj['continent'] == 'continent'
    assert jsonobj['country'] == "country"
    assert jsonobj['country_emoji'] == "country_emoji"
    assert jsonobj['region'] == "region"
    assert jsonobj['city'] == "city"
