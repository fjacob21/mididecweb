
class SqliteMalingList():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def add(self, user_id):
        self.insert_object(user_id)

    def get_all(self):
        try:
            r = self._conn.execute("select * from mailinglist")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            return []

    def delete(self, user_id):
        try:
            t = (user_id, )
            self._conn.execute("delete from mailinglist where user_id=?", t)
            self._conn.commit()
            return True
        except Exception as e:
            return False

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE mailinglist")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        member = {}
        member['user_id'] = rec[0]
        return member

    def insert_object(self, user_id):
        sql = "insert into mailinglist VALUES ("
        sql += '"' + user_id + '")'
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="mailinglist"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table mailinglist(user_id)")
        self._conn.commit()
