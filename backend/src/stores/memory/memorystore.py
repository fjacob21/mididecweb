from .memoryevents import MemoryEvents
from .memorywaitings import MemoryWaitings
from .memoryattendees import MemoryAttendees
from .memoryusers import MemoryUsers


class MemoryStore():

    def __init__(self):
        self.events = MemoryEvents()
        self.attendees = MemoryAttendees()
        self.waitings = MemoryWaitings()
        self.users = MemoryUsers()

    def reset(self):
        self.events.reset()
        self.attendees.reset()
        self.waitings.reset()
        self.users.reset()

    def clean(self):
        self.events.clean()
        self.attendees.clean()
        self.waitings.clean()
        self.users.clean()
