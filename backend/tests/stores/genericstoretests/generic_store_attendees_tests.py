
def test_attendees(attendees):
    attendees.add('user', 'event')
    assert len(attendees.get_all('event')) == 1
    attendee = attendees.get_all('event')[0]
    assert attendee
    assert attendee['user_id'] == 'user'
    assert attendee['event_id'] == 'event'
    attendees.delete('user', 'event')
    attendees.delete('user', 'event')

    attendees.add('user', 'event')
    attendees.reset()
    assert len(attendees.get_all('event')) == 0
    attendees.reset()

    attendees.add('user', 'event')
    attendees.clean()
    assert len(attendees.get_all('event')) == 0
    attendees.clean()
