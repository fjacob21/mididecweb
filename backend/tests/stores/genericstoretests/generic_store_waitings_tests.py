
def test_waitings(waitings):
    waitings.add('user', 'event')
    assert len(waitings.get_all('event')) == 1
    waiting = waitings.get_all('event')[0]
    assert waiting
    assert waiting['user_id'] == 'user'
    assert waiting['event_id'] == 'event'
    waitings.delete('user', 'event')
    waitings.delete('user', 'event')

    waitings.add('user', 'event')
    waitings.reset()
    assert len(waitings.get_all('event')) == 0
    waitings.reset()

    waitings.add('user', 'event')
    waitings.clean()
    assert len(waitings.get_all('event')) == 0
    waitings.clean()
