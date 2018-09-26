import sqlite3
from .sqliteevents import SqliteEvents
from .sqlitewaitings import SqliteWaitings
from .sqliteattendees import SqliteAttendees
from .sqliteattachments import SqliteAttachments
from .sqliteusers import SqliteUsers
from .sqlitelogins import SqliteLogins
from .sqlitelogs import SqliteLogs
from .sqlitepasswordresetrequests import SqlitePasswordResetRequests


class SqliteStore():

    def __init__(self, db='mididec.db'):
        self._db = db
        self._conn = sqlite3.connect(self._db)
        self.events = SqliteEvents(self._conn)
        self.attendees = SqliteAttendees(self._conn)
        self.waitings = SqliteWaitings(self._conn)
        self.attachments = SqliteAttachments(self._conn)
        self.users = SqliteUsers(self._conn)
        self.logins = SqliteLogins(self._conn)
        self.logs = SqliteLogs(self._conn)
        self.reset_password_requests = SqlitePasswordResetRequests(self._conn)

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

    def open(self):
        self._conn = sqlite3.connect(self._db)
        self.events._conn = self._conn
        self.attendees._conn = self._conn
        self.waitings._conn = self._conn
        self.attachments._conn = self._conn
        self.users._conn = self._conn
        self.logins._conn = self._conn
        self.logs._conn = self._conn
        self.reset_password_requests._conn = self._conn

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
        self.events.restore(backup)
        self.attendees.restore(backup)
        self.waitings.restore(backup)
        self.attachments.restore(backup)
        self.users.restore(backup)
        self.logins.restore(backup)
        self.logs.restore(backup)
        self.reset_password_requests.restore(backup)

    def close(self):
        self._conn.close()
