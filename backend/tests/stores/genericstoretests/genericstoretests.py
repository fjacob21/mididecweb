from .generic_store_object_tests import test_object
from .generic_store_events_tests import test_events
from .generic_store_attendees_tests import test_attendees
from .generic_store_users_tests import test_users


def store_tests(store):
    test_object(store)
    test_events(store.events)
    test_attendees(store.attendees)
    test_attendees(store.waitings)
    test_users(store.users)
