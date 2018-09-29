from datetime import datetime
import pytz
from .sqlitetable import SqliteTable


class SqliteEvents(SqliteTable):

    def __init__(self, conn):
        self._name = 'events'
        self._fields = [{'name': 'event_id', 'type': 'str', 'default': ''},
                        {'name': 'title', 'type': 'str', 'default': ''},
                        {'name': 'description', 'type': 'str', 'default': ''},
                        {'name': 'max_attendee', 'type': 'int', 'default': 20},
                        {'name': 'start', 'type': 'str', 'default': ''},
                        {'name': 'duration', 'type': 'int', 'default': 3600},
                        {'name': 'location', 'type': 'str', 'default': ''},
                        {'name': 'organizer_name', 'type': 'str', 'default': ''},
                        {'name': 'organizer_email', 'type': 'str', 'default': ''},
                        {'name': 'owner_id', 'type': 'str', 'default': ''},
                        {'name': 'create_date', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def create(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, event_id, owner_id):
        if not self.get(event_id):
            self.insert_object(title, description, max_attendee, start,
                               duration, location, organizer_name,
                               organizer_email, event_id, owner_id)

    def get_all(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception:
            return []

    def get(self, event_id):
        try:
            t = (event_id,)
            r = self._conn.execute("select * from {table} where event_id=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def update(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, event_id):
        event = self.get(event_id)
        if event:
            obj = (title, description, max_attendee, start,
                   duration, location, organizer_name,
                   organizer_email, event_id)
            try:
                sql = 'update {table} set '.format(table=self._name)
                sql += 'title=? ,'
                sql += 'description=? ,'
                sql += 'max_attendee=? ,'
                sql += 'start=? ,'
                sql += 'duration=? ,'
                sql += 'location=? ,'
                sql += 'organizer_name=? ,'
                sql += 'organizer_email=? '
                sql += 'where event_id=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
            except Exception:
                pass

    def delete(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from {table} where event_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception:
            pass

    def insert_object(self, title, description, max_attendee, start, duration,
                      location, organizer_name, organizer_email, event_id,
                      owner_id):
        create_date_dt = datetime.now(pytz.timezone("America/New_York"))
        create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + event_id + '", '
        sql += '"' + title + '", '
        sql += '"' + description + '", '
        sql += '"' + str(max_attendee) + '", '
        sql += '"' + start + '", '
        sql += '"' + str(int(duration)) + '", '
        sql += '"' + location + '", '
        sql += '"' + organizer_name + '", '
        sql += '"' + organizer_email + '", '
        sql += '"' + owner_id + '", '
        sql += '"' + create_date + '") '
        self._conn.execute(sql)
        self._conn.commit()
