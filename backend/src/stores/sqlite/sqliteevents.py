from datetime import datetime
import pytz


class SqliteEvents():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

    def create(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, event_id, owner_id):
        if not self.get(event_id):
            self.insert_object(title, description, max_attendee, start,
                               duration, location, organizer_name,
                               organizer_email, event_id, owner_id)

    def get_all(self):
        try:
            r = self._conn.execute("select * from events")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception:
            return []

    def get(self, event_id):
        try:
            t = (event_id,)
            r = self._conn.execute("select * from events where event_id=?", t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def update(self, title, description, max_attendee, start, duration,
               location, organizer_name, organizer_email, event_id):
        event = self.get(event_id)
        if event:
            obj = (title, description, max_attendee, start,
                   duration, location, organizer_name,
                   organizer_email, event_id)
            try:
                sql = 'update events set '
                sql += 'title=? ,'
                sql += 'description=? ,'
                sql += 'max_attendee=? ,'
                sql += 'start=? ,'
                sql += 'duration=? ,'
                sql += 'location=? ,'
                sql += 'organizer_name=? ,'
                sql += 'organizer_email=? '
                sql += 'where event_id=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
            except Exception:
                pass

    def delete(self, event_id):
        try:
            t = (event_id,)
            self._conn.execute("delete from events where event_id=?", t)
            self._conn.commit()
        except Exception:
            pass

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE events")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        event = {}
        event['event_id'] = rec[0]
        event['title'] = rec[1]
        event['description'] = rec[2]
        event['max_attendee'] = int(rec[3])
        event['start'] = rec[4]
        event['duration'] = int(rec[5])
        event['location'] = rec[6]
        event['organizer_name'] = rec[7]
        event['organizer_email'] = rec[8]
        event['owner_id'] = rec[9]
        event['create_date'] = rec[10]
        return event

    def insert_object(self, title, description, max_attendee, start, duration,
                      location, organizer_name, organizer_email, event_id,
                      owner_id):
        create_date_dt = datetime.now(pytz.timezone("America/New_York"))
        create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        sql = "insert into events VALUES ("
        sql += '"' + event_id + '", '
        sql += '"' + title + '", '
        sql += '"' + description + '", '
        sql += '"' + str(max_attendee) + '", '
        sql += '"' + start + '", '
        sql += '"' + str(int(duration)) + '", '
        sql += '"' + location + '", '
        sql += '"' + organizer_name + '", '
        sql += '"' + organizer_email + '", '
        sql += '"' + owner_id + '", '
        sql += '"' + create_date + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="events"')
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
                sql = "insert into events ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['event_id', 'title', 'description', 'max_attendee', 'start',
                'duration', 'location', 'organizer_name', 'organizer_email',
                'owner_id', 'create_date']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(events);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table events ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
