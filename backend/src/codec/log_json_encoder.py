import json


class LogJsonEncoder():

    def __init__(self, log):
        self._log = log

    def encode(self, format='string'):
        result = {}
        result['log_id'] = self._log.log_id
        result['ip'] = self._log.ip
        result['os'] = self._log.os
        result['os_version'] = self._log.os_version
        result['browser'] = self._log.browser
        result['browser_version'] = self._log.browser_version
        result['continent'] = self._log.continent
        result['continent'] = self._log.continent
        result['country'] = self._log.country
        result['country_emoji'] = self._log.country_emoji
        result['region'] = self._log.region
        result['city'] = self._log.city

        if format == 'dict':
            return result
        return json.dumps(result)
