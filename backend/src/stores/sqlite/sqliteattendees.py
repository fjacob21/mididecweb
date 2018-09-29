from .sqlitetable import SqliteTable


class SqliteAttendees(SqliteTable):

    def __init__(self, conn):
        self._name = 'attendees'
        self._fields = [{'name': 'user_id', 'type': 'str', 'default': ''},
                        {'name': 'event_id', 'type': 'str', 'default': ''}
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

    def insert_object(self, user_id, event_id):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + user_id + '", '
        sql += '"' + event_id + '")'
        self._conn.execute(sql)
        self._conn.commit()
