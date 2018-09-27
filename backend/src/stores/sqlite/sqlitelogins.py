
class SqliteLogins():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

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
        except Exception:
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
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="logins"')
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
                sql = "insert into logins ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['user_id', 'loginkey', 'ip']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(logins);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table logins ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
