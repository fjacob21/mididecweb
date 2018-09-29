from .sqlitetable import SqliteTable


class SqlitePasswordResetRequests(SqliteTable):

    def __init__(self, conn):
        self._name = 'reset_password_requests'
        self._fields = [{'name': 'request_id', 'type': 'str', 'default': ''},
                        {'name': 'date', 'type': 'str', 'default': ''},
                        {'name': 'username', 'type': 'str', 'default': ''},
                        {'name': 'email', 'type': 'str', 'default': ''},
                        {'name': 'accepted', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def create(self, request_id, date, username, email):
        if not self.get(request_id):
            self.insert_object(request_id, date, username, email)
            return self.get(request_id)

    def get_all(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('Except getall', e)
            return []

    def get(self, request_id):
        try:
            t = (request_id,)
            sql = 'select * from {table} where request_id=?'.format(table=self._name)
            r = self._conn.execute(sql, t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def update(self, request_id, date, username, email, accepted):
        req = self.get(request_id)
        if req:
            obj = (date, username, email, accepted)
            try:
                sql = 'update {table} set '.format(table=self._name)
                sql += 'date=? ,'
                sql += 'username=? ,'
                sql += 'email=? ,'
                sql += 'accepted=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
            except Exception:
                pass

    def delete(self, request_id):
        try:
            t = (request_id,)
            sql = 'delete from {table} where request_id=?'.format(table=self._name)
            self._conn.execute(sql, t)
            self._conn.commit()
        except Exception:
            pass

    def insert_object(self, request_id, date, username, email, accepted=''):
        try:
            sql = "insert into {table} VALUES (".format(table=self._name)
            sql += '"' + request_id + '", '
            sql += '"' + date + '", '
            sql += '"' + username + '", '
            sql += '"' + email + '", '
            sql += '"' + accepted + '") '
            self._conn.execute(sql)
            self._conn.commit()
        except Exception as e:
            print('insert ex', e)
