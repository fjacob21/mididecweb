from src.logs import Logs
from src.stores import MemoryStore


def generate_log(logs, is_eu=False):
    l = logs.add('0.0.0.0', 'os', '1.0.0', 'browser', '1.0.0', 'continent',
                 is_eu, 'country', 'country_emoji', 'region', 'city')
    return l


def test_log():
    store = MemoryStore()
    logs = Logs(store)
    l = generate_log(logs)
    assert l.ip == "0.0.0.0"
    assert l.os == "os"
    assert l.os_version == "1.0.0"
    assert l.browser == "browser"
    assert l.browser_version == "1.0.0"
    assert l.continent == "continent"
    assert l.country == "country"
    assert l.country_emoji == "country_emoji"
    assert l.region == "region"
    assert l.city == "city"
