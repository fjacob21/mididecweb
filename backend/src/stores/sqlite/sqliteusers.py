from .sqlitetable import SqliteTable
from datetime import datetime
import pytz


class SqliteUsers(SqliteTable):

    def __init__(self, conn):
        self._name = 'users'
        self._fields = [{'name': 'user_id', 'type': 'str', 'default': ''},
                        {'name': 'email', 'type': 'str', 'default': ''},
                        {'name': 'name', 'type': 'str', 'default': ''},
                        {'name': 'alias', 'type': 'str', 'default': ''},
                        {'name': 'psw', 'type': 'str', 'default': ''},
                        {'name': 'phone', 'type': 'str', 'default': ''},
                        {'name': 'useemail', 'type': 'bool', 'default': True},
                        {'name': 'usesms', 'type': 'bool', 'default': False},
                        {'name': 'profile', 'type': 'str', 'default': ''},
                        {'name': 'access', 'type': 'int', 'default': 0},
                        {'name': 'validated', 'type': 'bool', 'default': False},
                        {'name': 'smsvalidated', 'type': 'bool', 'default': False},
                        {'name': 'lastlogin', 'type': 'str', 'default': ''},
                        {'name': 'loginkey', 'type': 'str', 'default': ''},
                        {'name': 'avatar_path', 'type': 'str', 'default': ''},
                        {'name': 'create_date', 'type': 'str', 'default': ''},
                        {'name': 'smscode', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def create(self, user_id, email, name, alias, psw, phone, useemail, usesms,
               profile, access, validated=False, smsvalidated=False, lastlogin='', loginkey='', avatar_path='', smscode=''):
        if not self.get(user_id) and not self.find_email(email):
            self.insert_object(user_id, email, name, alias, psw, phone, useemail,
                               usesms, profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path, smscode)

    def get_all(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                try:
                    result.append(self.create_object(rec))
                except Exception as e:
                    print('user getall except', e)
            return result
        except Exception as e:
            print('user getall except', e)
            return []

    def find_email(self, email):
        for user in self.get_all():
            if user['email'] == email:
                return user
        return None

    def get(self, user_id):
        try:
            t = (user_id,)
            r = self._conn.execute("select * from {table} where user_id=?".format(table=self._name), t)
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
                sql = 'update {table} set '.format(table=self._name)
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
            self._conn.execute("delete from {table} where user_id=?".format(table=self._name), t)
            self._conn.commit()
        except Exception:
            pass

    def insert_object(self, user_id, email, name, alias, psw, phone, useemail, usesms,
                      profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path, smscode):
        create_date_dt = datetime.now(pytz.timezone("America/New_York"))
        create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        sql = "insert into {table} VALUES (".format(table=self._name)
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
