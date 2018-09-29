from .sqlitetable import SqliteTable


class SqliteAttachments(SqliteTable):

    def __init__(self, conn):
        self._name = 'attachments'
        self._fields = [{'name': 'path', 'type': 'str', 'default': ''},
                        {'name': 'event_id', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def add(self, path, event_id):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(path, event_id)

    def get_alls(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_alls', e)
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

    def delete(self, path, event_id):
        try:
            t = (path, event_id)
            self._conn.execute("delete from {table} where path=? and event_id=?".format(table=self._name), t)
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

    def insert_object(self, path, event_id):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + path + '", '
        sql += '"' + event_id + '")'
        self._conn.execute(sql)
        self._conn.commit()
