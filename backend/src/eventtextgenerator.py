from datetime import datetime, timedelta
import pytz
import locale


class EventTextGenerator():

    def __init__(self, event, short=True):
        self._event = event
        self._short = short
        self._startdt = self.generate_datetime(self._event.start)
        self._enddt = self.generate_datetime(self._event.end)
        try:
            locale.setlocale(locale.LC_ALL, 'fr_CA')
        except Exception:
            pass

    def generate(self):
        if self._short:
            return self.generate_short()
        return self.generate_long()

    def generate_short(self):
        text = 'MidiDecouverte ---\n'
        text += '\nTitre: ' + self._event.title
        text += '\nDate: ' + self.generate_date_string(self._startdt)
        text += '\nHeure: ' + self.generate_time_string(self._startdt)
        text += '\nDuree: ' + self.generate_timedelta_string(self._event.duration)
        return text

    def generate_long(self):
        text = 'MidiDecouverte ---\n'
        text += '\nTitre: ' + self._event.title
        text += '\nDate: ' + self.generate_date_string(self._startdt)
        text += '\nHeure: ' + self.generate_time_string(self._startdt)
        text += '\nDuree: ' + self.generate_timedelta_string(self._event.duration)
        return text

    def generate_datetime(self, dt):
        dt = datetime.strptime(self._event.start,
                               "%Y-%m-%dT%H:%M:%SZ")
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0,
                        tzinfo=pytz.timezone("America/New_York"))

    def generate_timedelta(self, td):
        return timedelta(seconds=int(td))

    def generate_date_string(self, dt):
        return dt.strftime("%A %d %B %Y")

    def generate_time_string(self, dt):
        return dt.strftime("%H:%M %Z")

    def generate_timedelta_string(self, td):
        return str(self.generate_timedelta(td))
