
def generate_event(events):
    events.create('test', 'test', 20, '2018-04-26T13:00:00Z', 3600, 'test',
                  'test', 'test@test.com', 'test', 'owner_id')


def test_events(events):
    test_events_event(events)
    test_update(events)
    test_delete(events)
    test_reset(events)
    test_clean(events)


def test_events_event(events):
    generate_event(events)
    assert len(events.get_all()) == 1
    event = events.get_all()[0]
    assert event
    assert events.get('test')
    assert event == events.get('test')
    assert event['event_id'] == 'test'
    assert event['title'] == 'test'
    assert event['description'] == 'test'
    assert event['max_attendee'] == 20
    assert event['start'] == '2018-04-26T13:00:00Z'
    assert event['duration'] == 3600
    assert event['location'] == 'test'
    assert event['organizer_name'] == 'test'
    assert event['organizer_email'] == 'test@test.com'
    assert event['owner_id'] == 'owner_id'
    assert 'create_date' in event
    events.delete('test')


def test_update(events):
    generate_event(events)
    events.update('test2', 'test', 20, '2018-04-26T13:00:00Z', 3600, 'test',
                  'test', 'test@test.com', 'test')
    assert len(events.get_all()) == 1
    event = events.get_all()[0]
    assert event
    assert event['title'] == 'test2'
    events.delete('test')


def test_delete(events):
    generate_event(events)
    events.delete('test')
    assert len(events.get_all()) == 0
    assert not events.get('test')
    events.delete('test')


def test_reset(events):
    generate_event(events)
    events.reset()
    assert len(events.get_all()) == 0
    assert not events.get('test')
    events.reset()


def test_clean(events):
    generate_event(events)
    events.clean()
    assert len(events.get_all()) == 0
    assert not events.get('test')
    events.clean()
