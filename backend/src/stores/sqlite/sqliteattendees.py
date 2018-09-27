
class SqliteAttendees():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

    def add(self, user_id, event_id):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(user_id, event_id)

    def get_alls(self):
        try:
            r = self._conn.execute("select * from attendees")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_all', e)
            return []

    def get_all(self, event_id):
        try:
            t = (event_id,)
            r = self._conn.execute("select * from attendees where event_id=?", t)
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_all', e)
            return []

    def delete(self, user_id, event_id):
        try:
            t = (user_id, event_id)
            self._conn.execute("delete from attendees where user_id=? and event_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def delete_event(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from attendees where event_id=?", t)
            self._conn.commit()
        except Exception as e:
            print('Delete event', e)

    def delete_user(self, user_id):
        try:
            t = (user_id,)
            self._conn.execute("delete from attendees where user_id=?", t)
            self._conn.commit()
        except Exception as e:
            print('Delete user', e)

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE attendees")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        attendee = {}
        attendee['user_id'] = rec[0]
        attendee['event_id'] = rec[1]
        return attendee

    def insert_object(self, user_id, event_id):
        sql = "insert into attendees VALUES ("
        sql += '"' + user_id + '", '
        sql += '"' + event_id + '")'
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="attendees"')
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
                sql = "insert into attendees ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['user_id', 'event_id']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(attendees);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table attendees ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
