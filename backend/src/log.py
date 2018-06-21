
class Log(object):

    def __init__(self, store, log_id):
        self._store = store
        self._log_id = log_id

    def get_data(self):
        return self._store.logs.get(self._log_id)

    def update_data(self, data):
        self._store.events.update(self._log_id, data['ip'],
                                  data['os'], data['os_version'],
                                  data['browser'], data['browser_version'],
                                  data['continent'], data['country'],
                                  data['country_emoji'], data['region'],
                                  data['city'])

    def __eq__(self, value):
        return self.get_data() == value.get_data()

    @property
    def log_id(self):
        return self.get_data()['log_id']

    @property
    def ip(self):
        return self.get_data()['ip']

    @property
    def os(self):
        return self.get_data()['os']

    @property
    def os_version(self):
        return self.get_data()['os_version']

    @property
    def browser(self):
        return self.get_data()['browser']

    @property
    def browser_version(self):
        return self.get_data()['browser_version']

    @property
    def continent(self):
        return self.get_data()['continent']

    @property
    def country(self):
        return self.get_data()['country']

    @property
    def country_emoji(self):
        return self.get_data()['country_emoji']

    @property
    def region(self):
        return self.get_data()['region']

    @property
    def city(self):
        return self.get_data()['city']
