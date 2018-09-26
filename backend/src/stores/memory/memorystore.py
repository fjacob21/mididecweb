from .memoryevents import MemoryEvents
from .memorywaitings import MemoryWaitings
from .memoryattendees import MemoryAttendees
from .memoryattachments import MemoryAttachments
from .memoryusers import MemoryUsers
from .memorylogins import MemoryLogins
from .memorylogs import MemoryLogs
from .memorypasswordresetrequests import MemoryPasswordResetRequests


class MemoryStore():

    def __init__(self):
        self.events = MemoryEvents()
        self.attendees = MemoryAttendees()
        self.waitings = MemoryWaitings()
        self.attachments = MemoryAttachments()
        self.users = MemoryUsers()
        self.logins = MemoryLogins()
        self.logs = MemoryLogs()
        self.reset_password_requests = MemoryPasswordResetRequests()

    def reset(self):
        self.events.reset()
        self.attendees.reset()
        self.waitings.reset()
        self.attachments.reset()
        self.users.reset()
        self.logins.reset()
        self.logs.reset()
        self.reset_password_requests.reset()

    def clean(self):
        self.events.clean()
        self.attendees.clean()
        self.waitings.clean()
        self.attachments.clean()
        self.users.clean()
        self.logins.clean()
        self.logs.clean()
        self.reset_password_requests.clean()

    def backup(self):
        tables = {}
        backup = self.events.backup()
        tables[backup[0]] = backup[1]
        backup = self.attendees.backup()
        tables[backup[0]] = backup[1]
        backup = self.waitings.backup()
        tables[backup[0]] = backup[1]
        backup = self.attachments.backup()
        tables[backup[0]] = backup[1]
        backup = self.users.backup()
        tables[backup[0]] = backup[1]
        backup = self.logins.backup()
        tables[backup[0]] = backup[1]
        backup = self.logs.backup()
        tables[backup[0]] = backup[1]
        backup = self.reset_password_requests.backup()
        tables[backup[0]] = backup[1]
        return tables

    def restore(self, backup):
        print(backup)
        self.events.restore(backup)
        self.attendees.restore(backup)
        self.waitings.restore(backup)
        self.attachments.restore(backup)
        self.users.restore(backup)
        self.logins.restore(backup)
        self.logs.restore(backup)
        self.reset_password_requests.restore(backup)
