from .generic_store_object_tests import test_object
from .generic_store_events_tests import test_events
from .generic_store_attendees_tests import test_attendees
from .generic_store_users_tests import test_users
from .generic_store_logins_tests import test_logins
from .generic_store_logs_tests import test_logs


def store_tests(store):
    test_object(store)
    store.reset()
    test_events(store.events)
    store.reset()
    test_attendees(store.attendees)
    store.reset()
    test_attendees(store.waitings)
    store.reset()
    test_users(store.users)
    store.reset()
    test_logins(store.logins)
    store.reset()
    test_logs(store.logs)
    store.reset()
