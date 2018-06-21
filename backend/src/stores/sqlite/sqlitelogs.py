

class SqliteLogs():

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()

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
        except Exception as e:
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
        self._conn.execute("create table logs(log_id, date, ip, os, os_version, browser, browser_version, continent, country, country_emoji, region, city)")
        self._conn.commit()
