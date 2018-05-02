def generate_user(users):
    users.create('test', 'test@test.com', 'test', 'test', 'psw', '1234567890', True,
                 False, 'profile', 8, True, True, '2018-04-26T13:00:00Z', 'testkey')


def test_users(users):
    test_users_user(users)
    test_update(users)
    test_delete(users)
    test_reset(users)
    test_clean(users)


def test_users_user(users):
    generate_user(users)
    assert len(users.get_all()) == 1
    user = users.get_all()[0]
    assert user
    assert users.get('test')
    assert user == users.get('test')
    assert user['user_id'] == 'test'
    assert user['email'] == 'test@test.com'
    assert user['name'] == 'test'
    assert user['alias'] == 'test'
    assert user['psw'] == 'psw'
    assert user['phone'] == '1234567890'
    assert user['useemail']
    assert not user['usesms']
    assert user['profile'] == 'profile'
    assert user['access'] == 8
    assert 'validated' in user
    assert type(user['validated']) == bool
    assert 'smsvalidated' in user
    assert type(user['smsvalidated']) == bool
    assert 'lastlogin' in user
    assert user['lastlogin'] == '2018-04-26T13:00:00Z'
    assert 'loginkey' in user
    assert user['loginkey'] == 'testkey'
    users.delete('test')


def test_update(users):
    generate_user(users)
    users.update('test', 'test@test.com', 'test2', 'test', 'psw', '1234567890', True,
                 False, 'profile', 8, True, True, '2018-04-26T13:00:00Z', 'testkey')
    assert len(users.get_all()) == 1
    user = users.get_all()[0]
    assert user
    assert user['name'] == 'test2'
    users.delete('test')


def test_delete(users):
    generate_user(users)
    users.delete('test')
    assert len(users.get_all()) == 0
    assert not users.get('test')
    users.delete('test')


def test_reset(users):
    generate_user(users)
    users.reset()
    assert len(users.get_all()) == 0
    assert not users.get('test')
    users.reset()


def test_clean(users):
    generate_user(users)
    users.clean()
    assert len(users.get_all()) == 0
    assert not users.get('test')
    users.clean()
