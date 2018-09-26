

class MemoryLogs():

    def __init__(self):
        self._logs = []

    def create(self, log_id, date, ip, os, os_version, browser, browser_version,
               continent, country, country_emoji, region, city):
        if not self.get(log_id):
            obj = self.create_object(log_id, date, ip, os, os_version, browser,
                                     browser_version, continent, country,
                                     country_emoji, region, city)
            self._logs.append(obj)

    def get_all(self):
        return self._logs

    def get(self, log_id):
        for log in self._logs:
            if log['log_id'] == log_id:
                return log
        return None

    def delete(self, log_id):
        idx = self.index(log_id)
        if idx != -1:
            del self._logs[idx]

    def reset(self):
        self._logs = []

    def clean(self):
        self.reset()

    def backup(self):
        return ('logs', self._logs)

    def restore(self, backup):
        self._logs = backup['logs']

    def create_object(self, log_id, date, ip, os, os_version, browser,
                      browser_version, continent, country, country_emoji,
                      region, city):
        log = {}
        log['log_id'] = log_id
        log['date'] = date
        log['ip'] = ip
        log['os'] = os
        log['os_version'] = os_version
        log['browser'] = browser
        log['browser_version'] = browser_version
        log['continent'] = continent
        log['country'] = country
        log['country_emoji'] = country_emoji
        log['region'] = region
        log['city'] = city
        return log

    def index(self, log_id):
        i = 0
        for log in self._logs:
            if log['log_id'] == log_id:
                return i
            i += 1
        return -1
