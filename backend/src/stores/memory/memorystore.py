from .memoryevents import MemoryEvents
from .memorywaitings import MemoryWaitings
from .memoryattendees import MemoryAttendees
from .memoryusers import MemoryUsers
from .memorylogins import MemoryLogins
from .memorylogs import MemoryLogs


class MemoryStore():

    def __init__(self):
        self.events = MemoryEvents()
        self.attendees = MemoryAttendees()
        self.waitings = MemoryWaitings()
        self.users = MemoryUsers()
        self.logins = MemoryLogins()
        self.logs = MemoryLogs()

    def reset(self):
        self.events.reset()
        self.attendees.reset()
        self.waitings.reset()
        self.users.reset()
        self.logins.reset()
        self.logs.reset()

    def clean(self):
        self.events.clean()
        self.attendees.clean()
        self.waitings.clean()
        self.users.clean()
        self.logins.clean()
        self.logs.clean()
