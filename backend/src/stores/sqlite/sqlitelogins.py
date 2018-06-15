
class SqliteLogins():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def add(self, user_id, loginkey, ip):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(user_id, loginkey, ip)

    def get(self, loginkey):
        try:
            t = (loginkey,)
            r = self._conn.execute("select * from logins where loginkey=?", t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            t = (user_id,)
            r = self._conn.execute("select * from logins where user_id=?", t)
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
            r = self._conn.execute("select * from logins")
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
            self._conn.execute("delete from logins where loginkey=?", t)
            self._conn.commit()
            print('deleted logins', loginkey)
        except Exception as e:
            print(e)

    def delete_user(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from logins where user_id=?", t)
            self._conn.commit()
        except Exception as e:
            print('Delete user', e)

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE logins")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        login = {}
        login['user_id'] = rec[0]
        login['loginkey'] = rec[1]
        login['ip'] = rec[2]
        return login

    def insert_object(self, user_id, loginkey, ip):
        sql = "insert into logins VALUES ("
        sql += '"' + user_id + '", '
        sql += '"' + loginkey + '", '
        sql += '"' + ip + '")'
        print(sql)
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="logins"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table logins(user_id, loginkey, ip)")
        self._conn.commit()
