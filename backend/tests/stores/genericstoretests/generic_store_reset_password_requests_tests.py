
def generate_request(passwordresetrequests):
    r = passwordresetrequests.create('test', 'date', 'username', 'email')
    return r


def test_reset_password_requests(passwordresetrequests):
    test_create(passwordresetrequests)
    test_get_all(passwordresetrequests)
    test_get(passwordresetrequests)
    test_item(passwordresetrequests)
    test_reset(passwordresetrequests)
    test_clean(passwordresetrequests)


def test_create(passwordresetrequests):
    generate_request(passwordresetrequests)
    assert len(passwordresetrequests.get_all()) == 1
    passwordresetrequests.reset()


def test_get_all(passwordresetrequests):
    req = generate_request(passwordresetrequests)
    assert len(passwordresetrequests.get_all()) == 1
    request = passwordresetrequests.get_all()[0]
    assert request
    assert request == req
    passwordresetrequests.reset()


def test_get(passwordresetrequests):
    req = generate_request(passwordresetrequests)
    assert len(passwordresetrequests.get_all()) == 1
    request = passwordresetrequests.get_all()[0]
    assert request
    assert request == req
    assert passwordresetrequests.get('test')
    assert request == passwordresetrequests.get('test')
    assert request['request_id'] == 'test'
    assert request['date'] == 'date'
    assert request['username'] == 'username'
    assert request['email'] == 'email'
    passwordresetrequests.reset()


def test_item(passwordresetrequests):
    req = generate_request(passwordresetrequests)
    assert req
    assert 'request_id' in req
    assert req['request_id'] == 'test'
    assert 'date' in req
    assert req['date'] == 'date'
    assert 'username' in req
    assert req['username'] == 'username'
    assert 'email' in req
    assert req['email'] == 'email'
    assert 'accepted' in req
    assert req['accepted'] == ''
    passwordresetrequests.reset()


def test_update(passwordresetrequests):
    request = generate_request(passwordresetrequests)
    request.update('test2', 'date2', 'username2', 'email2', 'accepted2')
    assert len(passwordresetrequests.get_all()) == 1
    request = passwordresetrequests.get_all()[0]
    assert request
    assert request['request_id'] == 'test2'
    assert request['date'] == 'date2'
    assert request['username'] == 'username2'
    assert request['email'] == 'email2'
    assert request['accepted'] == 'accepted2'
    passwordresetrequests.reset()


def test_delete(passwordresetrequests):
    generate_request(passwordresetrequests)
    assert len(passwordresetrequests.get_all()) == 1
    request = passwordresetrequests.get_all()[0]
    passwordresetrequests.delete(request['request_id'])
    assert len(passwordresetrequests.get_all()) == 0
    passwordresetrequests.reset()


def test_reset(passwordresetrequests):
    generate_request(passwordresetrequests)
    passwordresetrequests.reset()
    assert len(passwordresetrequests.get_all()) == 0
    assert not passwordresetrequests.get('test')
    passwordresetrequests.reset()


def test_clean(passwordresetrequests):
    generate_request(passwordresetrequests)
    passwordresetrequests.clean()
    assert len(passwordresetrequests.get_all()) == 0
    assert not passwordresetrequests.get('test')
    passwordresetrequests.reset()
