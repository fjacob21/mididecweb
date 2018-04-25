def test_object(store):
    test_store_object(store)
    test_events_object(store.events)
    test_attendees_object(store.attendees)
    test_attendees_object(store.waitings)
    test_users_object(store.users)


def test_store_object(store):
    assert store
    assert store.events
    assert store.attendees
    assert store.waitings
    assert store.users
    assert store.reset
    assert store.clean


def test_events_object(events):
    assert events.create
    assert events.get_all
    assert events.get
    assert events.update
    assert events.delete
    assert events.reset
    assert events.clean


def test_attendees_object(attendees):
    assert attendees.add
    assert attendees.get_all
    assert attendees.delete
    assert attendees.reset
    assert attendees.clean


def test_users_object(users):
    assert users.create
    assert users.get_all
    assert users.get
    assert users.update
    assert users.delete
    assert users.reset
    assert users.clean
