from .sqlitetable import SqliteTable
from datetime import datetime, timedelta
import pytz


class SqliteAttendees(SqliteTable):

    def __init__(self, conn):
        self._name = 'attendees'
        self._fields = [{'name': 'user_id', 'type': 'str', 'default': ''},
                        {'name': 'event_id', 'type': 'str', 'default': ''},
                        {'name': 'present', 'type': 'bool', 'default': False},
                        {'name': 'present_time', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def add(self, user_id, event_id):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(user_id, event_id)

    def get_alls(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_all', e)
            return []

    def get_all(self, event_id):
        try:
            t = (event_id,)
            r = self._conn.execute("select * from {table} where event_id=?".format(table=self._name), t)
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_all', e)
            return []
    
    def get(self, user_id, event_id):
        try:
            t = (user_id, event_id,)
            r = self._conn.execute("select * from {table} where user_id=? and event_id=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception as e:
            print('get', e)
            return None

    def delete(self, user_id, event_id):
        try:
            t = (user_id, event_id)
            self._conn.execute("delete from {table} where user_id=? and event_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception:
            pass

    def delete_event(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from {table} where event_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception as e:
            print('Delete event', e)

    def delete_user(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from {table} where user_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception as e:
            print('Delete user', e)

    def update(self, user_id, event_id, present):
        if present:
            start = datetime.now(pytz.timezone("America/New_York"))
            startstr = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            startstr = ''

        event = self.get(user_id, event_id)
        if event:
            obj = (str(present), startstr, event_id, user_id)
            print('Update attendees', obj)
            try:
                sql = 'update {table} set '.format(table=self._name)
                sql += 'present=? ,'
                sql += 'present_time=?'
                sql += 'where event_id=? and user_id=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
                return True
            except Exception as e:
                print('Update event except', e)
                return False

    def insert_object(self, user_id, event_id, present=False, present_time=''):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + user_id + '", '
        sql += '"' + event_id + '", '
        sql += '"' + str(present) + '", '
        sql += '"' + present_time + '")'
        self._conn.execute(sql)
        self._conn.commit()
