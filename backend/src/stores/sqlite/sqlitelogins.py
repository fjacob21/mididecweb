from .sqlitetable import SqliteTable


class SqliteLogins(SqliteTable):

    def __init__(self, conn):
        self._name = 'logins'
        self._fields = [{'name': 'user_id', 'type': 'str', 'default': ''},
                        {'name': 'loginkey', 'type': 'str', 'default': ''},
                        {'name': 'ip', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def add(self, user_id, loginkey, ip):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(user_id, loginkey, ip)

    def get(self, loginkey):
        try:
            t = (loginkey,)
            r = self._conn.execute("select * from {table} where loginkey=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            t = (user_id,)
            r = self._conn.execute("select * from {table} where user_id=?".format(table=self._name), t)
            res = r.fetchall()
            result = []
            for rec in res:
                try:
                    result.append(self.create_object(rec))
                except Exception:
                    pass
            return result
        except Exception as e:
            print(e)
            return []

    def get_all(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                try:
                    result.append(self.create_object(rec))
                except Exception:
                    pass
            return result
        except Exception as e:
            print(e)
            return []

    def delete(self, loginkey):
        try:
            t = (loginkey,)
            self._conn.execute("delete from {table} where loginkey=?".format(table=self._name), t)
            self._conn.commit()
        except Exception as e:
            print(e)

    def delete_user(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from {table} where user_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception as e:
            print('Delete user', e)

    def insert_object(self, user_id, loginkey, ip):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + user_id + '", '
        sql += '"' + loginkey + '", '
        sql += '"' + ip + '")'
        self._conn.execute(sql)
        self._conn.commit()
