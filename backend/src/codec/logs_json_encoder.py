import json
from .log_json_encoder import LogJsonEncoder


class LogsJsonEncoder():

    def __init__(self, logs):
        self._logs = logs

    def encode(self, format='string'):
        result = {}
        result['count'] = self._logs.count
        logs = []
        for log in self._logs.list:
            logs.append(LogJsonEncoder(log).encode('dict'))
        result['logs'] = logs
        if format == 'dict':
            return result
        return json.dumps(result)
