

class SqlitePasswordResetRequests():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def create(self, request_id, date, username, email):
        if not self.get(request_id):
            self.insert_object(request_id, date, username, email)
            print('sql create', self.get(request_id))
            return self.get(request_id)

    def get_all(self):
        try:
            r = self._conn.execute("select * from reset_password_requests")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            return []

    def get(self, request_id):
        try:
            t = (request_id,)
            r = self._conn.execute("select * from reset_password_requests where request_id=?", t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def delete(self, request_id):
        try:
            t = (request_id,)
            self._conn.execute("delete from reset_password_requests where request_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE reset_password_requests")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        request = {}
        request['request_id'] = rec[0]
        request['date'] = rec[1]
        request['username'] = rec[2]
        request['email'] = rec[3]
        request['accepted'] = rec[4]
        return request

    def insert_object(self, request_id, date, username, email, accepted=''):
        sql = "insert into reset_password_requests VALUES ("
        sql += '"' + request_id + '", '
        sql += '"' + date + '", '
        sql += '"' + username + '", '
        sql += '"' + email + '", '
        sql += '"' + accepted + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="reset_password_requests"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table reset_password_requests(request_id, date, username, email, accepted)")
        self._conn.commit()
