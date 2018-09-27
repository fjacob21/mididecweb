

class SqliteLogs():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

    def create(self, log_id, date, ip, os, os_version, browser, browser_version,
               continent, country, country_emoji, region, city):
        if not self.get(log_id):
            self.insert_object(log_id, date, ip, os, os_version, browser,
                               browser_version, continent, country,
                               country_emoji, region, city)

    def get_all(self):
        try:
            r = self._conn.execute("select * from logs")
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception:
            return []

    def get(self, log_id):
        try:
            t = (log_id,)
            r = self._conn.execute("select * from logs where log_id=?", t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE logs")
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        event = {}
        event['log_id'] = rec[0]
        event['date'] = rec[1]
        event['ip'] = rec[2]
        event['os'] = rec[3]
        event['os_version'] = rec[4]
        event['browser'] = rec[5]
        event['browser_version'] = rec[6]
        event['continent'] = rec[7]
        event['country'] = rec[8]
        event['country_emoji'] = rec[9]
        event['region'] = rec[10]
        event['city'] = rec[11]
        return event

    def insert_object(self, log_id, date, ip, os, os_version, browser,
                      browser_version, continent, country, country_emoji,
                      region, city):
        sql = "insert into logs VALUES ("
        sql += '"' + log_id + '", '
        sql += '"' + date + '", '
        sql += '"' + ip + '", '
        sql += '"' + os + '", '
        sql += '"' + os_version + '", '
        sql += '"' + browser + '", '
        sql += '"' + browser_version + '", '
        sql += '"' + continent + '", '
        sql += '"' + country + '", '
        sql += '"' + country_emoji + '", '
        sql += '"' + region + '", '
        sql += '"' + city + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="logs"')
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
                sql = "insert into logs ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        return ['log_id', 'date', 'ip', 'os', 'os_version', 'browser',
                'browser_version', 'continent', 'country', 'country_emoji',
                'region', 'city']

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info(logs);')
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table logs ('
        for field in self._get_fields():
            sql += field + ', '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        return sql
