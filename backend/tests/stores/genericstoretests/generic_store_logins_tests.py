
def test_logins(logins):
    logins.add('user', 'key', 'ip')
    logins.delete('key')
    assert not logins.get('key')

    logins.add('user', 'key', 'ip')
    logins.reset()
    assert len(logins.get_all()) == 0
    logins.reset()

    logins.add('user', 'key', 'ip')
    logins.clean()
    assert len(logins.get_all()) == 0
    logins.clean()
