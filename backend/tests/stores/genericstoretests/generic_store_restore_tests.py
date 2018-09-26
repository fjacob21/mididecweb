
def generate_event(events):
    events.create('test', 'test', 20, '2018-04-26T13:00:00Z', 3600, 'test',
                  'test', 'test@test.com', 'test', 'owner_id')


def generate_log(logs):
    logs.create('test', '123', '0.0.0.0', 'os', '1.0.0', 'browser', '1.0.0',
                'continent', 'country', 'country_emoji', 'region', 'city')


def generate_request(passwordresetrequests):
    r = passwordresetrequests.create('test', 'date', 'username', 'email')
    return r


def generate_user(users):
    users.create('test', 'test@test.com', 'test', 'test', 'psw', '1234567890',
                 True, False, 'profile', 8, True, True, '2018-04-26T13:00:00Z',
                 'testkey', 'avatar', 'smscode')


def test_restore(store):
    store.attendees.add('user', 'event')
    store.waitings.add('user', 'event')
    store.attachments.add('path', 'event')
    store.logins.add('user', 'key', 'ip')
    generate_event(store.events)
    generate_log(store.logs)
    generate_request(store.reset_password_requests)
    generate_user(store.users)
    backup = store.backup()
    store.reset()
    store.restore(backup)
    assert len(store.events.get_all()) == len(backup['events'])
    assert len(store.attendees.get_alls()) == len(backup['attendees'])
    assert len(store.attachments.get_alls()) == len(backup['attachments'])
    assert len(store.waitings.get_alls()) == len(backup['waitings'])
    assert len(store.users.get_all()) == len(backup['users'])
