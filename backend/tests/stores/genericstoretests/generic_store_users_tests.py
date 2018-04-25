def generate_user(users):
    users.create('test', 'test@test.com', 'test', 'test', '1234567890', True,
                 False, 'profile', True)


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
    assert user['phone'] == '1234567890'
    assert user['useemail']
    assert not user['usesms']
    assert user['profile'] == 'profile'
    assert user['validated']
    users.delete('test')


def test_update(users):
    generate_user(users)
    users.update('test', 'test@test.com', 'test2', 'test', '1234567890', True,
                 False, 'profile', True)
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
