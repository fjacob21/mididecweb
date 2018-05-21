
class SqliteWaitings():

    def __init__(self, conn):
        self._conn = conn

    def add(self, user_id, event_id):
        self.insert_object(user_id, event_id)

    def get_all(self, event_id):
        try:
            t = (event_id, )
            r = self._conn.execute("select * from waitings where event_id=?", t)
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            return []

    def delete(self, user_id, event_id):
        try:
            t = (user_id, event_id)
            self._conn.execute("delete from waitings where user_id=? and event_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def delete_event(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from waitings where event_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def delete_user(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from waitings where user_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE waitings")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        attendee = {}
        attendee['user_id'] = rec[0]
        attendee['event_id'] = rec[1]
        return attendee

    def insert_object(self, user_id, event_id):
        sql = "insert into waitings VALUES ("
        sql += '"' + user_id + '", '
        sql += '"' + event_id + '")'
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="waitings"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table waitings(user_id, event_id)")
        self._conn.commit()
