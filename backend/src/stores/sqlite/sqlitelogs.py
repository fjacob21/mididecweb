from .sqlitetable import SqliteTable


class SqliteLogs(SqliteTable):

    def __init__(self, conn):
        self._name = 'logs'
        self._fields = [{'name': 'log_id', 'type': 'str', 'default': ''},
                        {'name': 'date', 'type': 'str', 'default': ''},
                        {'name': 'ip', 'type': 'str', 'default': ''},
                        {'name': 'os', 'type': 'str', 'default': ''},
                        {'name': 'os_version', 'type': 'str', 'default': ''},
                        {'name': 'browser', 'type': 'str', 'default': ''},
                        {'name': 'browser_version', 'type': 'str', 'default': ''},
                        {'name': 'continent', 'type': 'str', 'default': ''},
                        {'name': 'country', 'type': 'str', 'default': ''},
                        {'name': 'country_emoji', 'type': 'str', 'default': ''},
                        {'name': 'region', 'type': 'str', 'default': ''},
                        {'name': 'city', 'type': 'str', 'default': ''}
                        ]
        super().__init__(conn)

    def create(self, log_id, date, ip, os, os_version, browser, browser_version,
               continent, country, country_emoji, region, city):
        if not self.get(log_id):
            self.insert_object(log_id, date, ip, os, os_version, browser,
                               browser_version, continent, country,
                               country_emoji, region, city)

    def get_all(self):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('Exception', e)
            return []

    def get(self, log_id):
        try:
            t = (log_id,)
            r = self._conn.execute("select * from {table} where log_id=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception:
            return None

    def insert_object(self, log_id, date, ip, os, os_version, browser,
                      browser_version, continent, country, country_emoji,
                      region, city):
        sql = "insert into {table} VALUES (".format(table=self._name)
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
