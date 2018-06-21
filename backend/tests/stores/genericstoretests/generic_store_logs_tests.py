
def generate_log(logs):
    logs.create('test', '123', '0.0.0.0', 'os', '1.0.0', 'browser', '1.0.0', 'continent',
                'country', 'country_emoji', 'region', 'city')


def test_logs(logs):
    test_logs_log(logs)
    test_reset(logs)
    test_clean(logs)


def test_logs_log(logs):
    generate_log(logs)
    assert len(logs.get_all()) == 1
    log = logs.get_all()[0]
    assert log
    assert logs.get('test')
    assert log == logs.get('test')
    assert log['log_id'] == 'test'
    assert log['date'] == '123'
    assert log['ip'] == '0.0.0.0'
    assert log['os'] == 'os'
    assert log['os_version'] == '1.0.0'
    assert log['browser'] == 'browser'
    assert log['browser_version'] == '1.0.0'
    assert log['continent'] == 'continent'
    assert log['country'] == 'country'
    assert log['country_emoji'] == 'country_emoji'
    assert log['region'] == 'region'
    assert log['city'] == 'city'


def test_reset(logs):
    generate_log(logs)
    logs.reset()
    assert len(logs.get_all()) == 0
    assert not logs.get('test')
    logs.reset()


def test_clean(logs):
    generate_log(logs)
    logs.clean()
    assert len(logs.get_all()) == 0
    assert not logs.get('test')
    logs.clean()
