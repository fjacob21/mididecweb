

class SqlitePasswordResetRequests():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def create(self, request_id, date, username, email):
        if not self.get(request_id):
            self.insert_object(request_id, date, username, email)
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
            print('getall', e)
            return []

    def get(self, request_id):
        try:
            t = (request_id,)
            sql = 'select * from reset_password_requests where request_id=?'
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
                sql = 'update reset_password_requests set '
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
            sql = 'delete from reset_password_requests where request_id=?'
            self._conn.execute(sql, t)
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
        try:
            sql = "insert into reset_password_requests VALUES ("
            sql += '"' + request_id + '", '
            sql += '"' + date + '", '
            sql += '"' + username + '", '
            sql += '"' + email + '", '
            sql += '"' + accepted + '") '
            self._conn.execute(sql)
            self._conn.commit()
        except Exception as e:
            print('insert ex', e)

    def is_table_exist(self):
        try:
            sql = 'SELECT name FROM sqlite_master '
            sql += 'where type="table" and name="reset_password_requests"'
            r = self._conn.execute(sql)
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        sql = 'create table reset_password_requests'
        sql += '(request_id, date, username, email, accepted)'
        self._conn.execute(sql)
        self._conn.commit()
