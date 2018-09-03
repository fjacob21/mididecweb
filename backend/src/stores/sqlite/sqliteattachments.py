
class SqliteAttachments():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

    def add(self, path, event_id):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(path, event_id)

    def get_all(self, event_id):
        try:
            t = (event_id,)
            r = self._conn.execute("select * from attachments where event_id=?", t)
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_all', e)
            return []

    def delete(self, path, event_id):
        try:
            t = (path, event_id)
            self._conn.execute("delete from attachments where path=? and event_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def delete_event(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from attachments where event_id=?", t)
            self._conn.commit()
        except Exception as e:
            print('Delete event', e)

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE attachments")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        attendee = {}
        attendee['path'] = rec[0]
        attendee['event_id'] = rec[1]
        return attendee

    def insert_object(self, path, event_id):
        sql = "insert into attachments VALUES ("
        sql += '"' + path + '", '
        sql += '"' + event_id + '")'
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="attachments"')
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute("create table attachments(path, event_id)")
        self._conn.commit()
