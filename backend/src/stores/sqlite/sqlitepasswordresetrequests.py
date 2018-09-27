

class SqlitePasswordResetRequests():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

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
        self._conn.execute(self._get_create_string())
        self._conn.commit()

    def update_schema(self):
        fields = self._get_fields()
        dbfields = self._get_db_fields()
        if len(fields) != len(dbfields):
            print('Need to update schema')
            recs = self.get_all()
            self.reset()
            for rec in recs:
                create_fields = ''
                values = ''
                for field in list(rec):
                    if field in fields:
                        create_fields += field + ','
                        values += '"' + str(rec[field]) + '",'
                create_fields = create_fields[:-1]
                values = values[:-1]
                sql = "insert into reset_password_requests ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['request_id', 'date', 'username', 'email', 'accepted']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(reset_password_requests);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table reset_password_requests ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
