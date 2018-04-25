from src.stores.memory import MemoryStore
from genericstoretests import store_tests


def test_memory_store():
    store = MemoryStore()
    store_tests(store)
