from datetime import datetime
import pytz


class SqliteUsers():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

    def create(self, user_id, email, name, alias, psw, phone, useemail, usesms,
               profile, access, validated=False, smsvalidated=False, lastlogin='', loginkey='', avatar_path='', smscode=''):
        if not self.get(user_id) and not self.find_email(email):
            self.insert_object(user_id, email, name, alias, psw, phone, useemail,
                               usesms, profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path, smscode)

    def get_all(self):
        try:
            r = self._conn.execute("select * from users")
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

    def find_email(self, email):
        for user in self.get_all():
            if user['email'] == email:
                return user
        return None

    def get(self, user_id):
        try:
            t = (user_id,)
            r = self._conn.execute("select * from users where user_id=?", t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception as e:
            return None

    def update(self, user_id, email, name, alias, psw, phone, useemail, usesms,
               profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path, smscode):
        user = self.get(user_id)
        if user:
            obj = (email, name, alias, psw,
                   phone, str(useemail), str(usesms),
                   profile, str(access), str(validated), str(smsvalidated), lastlogin, loginkey, avatar_path, smscode, user_id, )
            try:
                sql = 'update users set '
                sql += 'email=? ,'
                sql += 'name=? ,'
                sql += 'alias=? ,'
                sql += 'psw=? ,'
                sql += 'phone=? ,'
                sql += 'useemail=? ,'
                sql += 'usesms=? ,'
                sql += 'profile=? ,'
                sql += 'access=? ,'
                sql += 'validated=? ,'
                sql += 'smsvalidated=? ,'
                sql += 'lastlogin=? ,'
                sql += 'loginkey=? ,'
                sql += 'avatar_path=?, '
                sql += 'smscode=? '
                sql += 'where user_id=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
            except Exception as e:
                print('excep updatet', e)

    def delete(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from users where user_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE users")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        user = {}
        try:
            user['user_id'] = rec[0]
            user['email'] = rec[1]
            user['name'] = rec[2]
            user['alias'] = rec[3]
            user['psw'] = rec[4]
            user['phone'] = rec[5]
            user['useemail'] = eval(rec[6])
            user['usesms'] = eval(rec[7])
            user['profile'] = rec[8]
            user['access'] = int(rec[9])
            user['validated'] = eval(rec[10])
            user['smsvalidated'] = eval(rec[11])
            user['lastlogin'] = rec[12]
            user['loginkey'] = rec[13]
            user['avatar_path'] = rec[14]
            user['create_date'] = rec[15]
            user['smscode'] = rec[16]
        except Exception as e:
            print('create_object', e, rec[0], rec[2])
            raise e
        return user

    def insert_object(self, user_id, email, name, alias, psw, phone, useemail, usesms,
                      profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path, smscode):
        create_date_dt = datetime.now(pytz.timezone("America/New_York"))
        create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        sql = "insert into users VALUES ("
        sql += '"' + user_id + '", '
        sql += '"' + email + '", '
        sql += '"' + name + '", '
        sql += '"' + alias + '", '
        sql += '"' + psw + '", '
        sql += '"' + phone + '", '
        sql += '"' + str(useemail) + '", '
        sql += '"' + str(usesms) + '", '
        sql += '"' + profile + '", '
        sql += '"' + str(access) + '", '
        sql += '"' + str(validated) + '", '
        sql += '"' + str(smsvalidated) + '", '
        sql += '"' + lastlogin + '", '
        sql += '"' + loginkey + '", '
        sql += '"' + avatar_path + '", '
        sql += '"' + create_date + '", '
        sql += '"' + smscode + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="users"')
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
                sql = "insert into users ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['user_id', 'email', 'name', 'alias', 'psw', 'phone',
                'useemail', 'usesms', 'profile', 'access', 'validated',
                'smsvalidated', 'lastlogin', 'loginkey', 'avatar_path',
                'create_date', 'smscode']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(users);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table users ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
