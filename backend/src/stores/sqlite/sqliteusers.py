
class SqliteUsers():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def create(self, user_id, email, name, alias, phone, useemail, usesms,
               profile, validated):
        if not self.get(user_id) and not self.find_email(email):
            self.insert_object(user_id, email, name, alias, phone, useemail,
                               usesms, profile, validated)

    def get_all(self):
        try:
            r = self._conn.execute("select * from users")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
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

    def update(self, user_id, email, name, alias, phone, useemail, usesms,
               profile, validated):
        user = self.get(user_id)
        if user:
            obj = (email, name, alias,
                   phone, str(useemail), str(usesms),
                   profile, str(validated), user_id)
            try:
                sql = 'update users set '
                sql += 'email=? ,'
                sql += 'name=? ,'
                sql += 'alias=? ,'
                sql += 'phone=? ,'
                sql += 'useemail=? ,'
                sql += 'usesms=? ,'
                sql += 'profile=? ,'
                sql += 'validated=? '
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
        user['user_id'] = rec[0]
        user['email'] = rec[1]
        user['name'] = rec[2]
        user['alias'] = rec[3]
        user['phone'] = rec[4]
        user['useemail'] = eval(rec[5])
        user['usesms'] = eval(rec[6])
        user['profile'] = rec[7]
        user['validated'] = eval(rec[8])
        return user

    def insert_object(self, user_id, email, name, alias, phone, useemail, usesms,
                      profile, validated):
        sql = "insert into users VALUES ("
        sql += '"' + user_id + '", '
        sql += '"' + email + '", '
        sql += '"' + name + '", '
        sql += '"' + alias + '", '
        sql += '"' + phone + '", '
        sql += '"' + str(useemail) + '", '
        sql += '"' + str(usesms) + '", '
        sql += '"' + profile + '", '
        sql += '"' + str(validated) + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="users"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table users(user_id, email, name, alias, phone, useemail, usesms, profile, validated)")
        self._conn.commit()
