import datetime
from log import Log
import hashlib
import random


class Logs(object):

    def __init__(self, store):
        self._store = store

    def add(self, ip, os, os_version, browser, browser_version, continent, is_eu, country, country_emoji, region, city):
        if not is_eu and continent and country and region and city:
            date = datetime.datetime.now()
            datestr = date.strftime("%Y-%m-%dT%H:%M:%SZ")
            log_id = self.generate_log_id(ip, date)
            if not continent:
                continent = ''
            if not country:
                country = ''
            if not country_emoji:
                country_emoji = ''
            if not region:
                region = ''
            if not city:
                city = ''
            self._store.logs.create(log_id, datestr, ip, os, os_version,
                                    browser, browser_version, continent,
                                    country, country_emoji, region, city)
            return Log(self._store, log_id)

    def generate_log_id(self, ip, date):
        hash = hashlib.sha256()
        salt = str(random.randint(1, 1000))
        datestr = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        hash.update((datestr + ip + salt).encode())
        return hash.hexdigest()

    @property
    def list(self):
        result = []
        logs = self._store.logs.get_all()
        for log in logs:
            result.append(Log(self._store, log['log_id']))
        return result

    @property
    def count(self):
        return len(self.list)
