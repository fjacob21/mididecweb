from src.stores.memory import MemoryStore
from src.stores.sqlite import SqliteStore
from genericstoretests import store_tests


def test_memory_store():
    store = MemoryStore()
    store_tests(store)


def test_sqlite_store():
    store = SqliteStore()
    store_tests(store)
