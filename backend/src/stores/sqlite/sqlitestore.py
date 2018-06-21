import sqlite3
from .sqliteevents import SqliteEvents
from .sqlitewaitings import SqliteWaitings
from .sqliteattendees import SqliteAttendees
from .sqliteusers import SqliteUsers
from .sqlitelogins import SqliteLogins
from .sqlitelogs import SqliteLogs


class SqliteStore():

    def __init__(self, db='mididec.db'):
        self._db = db
        self._conn = sqlite3.connect(self._db)
        self.events = SqliteEvents(self._conn)
        self.attendees = SqliteAttendees(self._conn)
        self.waitings = SqliteWaitings(self._conn)
        self.users = SqliteUsers(self._conn)
        self.logins = SqliteLogins(self._conn)
        self.logs = SqliteLogs(self._conn)

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

    def open(self):
        self._conn = sqlite3.connect(self._db)
        self.events._conn = self._conn
        self.attendees._conn = self._conn
        self.waitings._conn = self._conn
        self.users._conn = self._conn
        self.logins._conn = self._conn
        self.logs._conn = self._conn

    def close(self):
        self._conn.close()
