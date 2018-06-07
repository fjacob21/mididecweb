from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta, timezone
import pytz


class iCalGenerator():

    def __init__(self, event):
        self._event = event
        self._startdt = self.generate_datetime(self._event.start)
        self._enddt = self.generate_datetime(self._event.end)

    def generate(self):
        cal = self.generate_calendar()
        ev = self.generate_event()
        alarm = self.generate_alarm()
        ev.add_component(alarm)
        organizer = self.generate_organizer()
        cal.add('organizer', organizer)
        cal.add_component(ev)
        return cal.to_ical().decode()

    def generate_calendar(self):
        cal = Calendar()
        cal.add('dtstart', self._startdt)
        cal.add('summary', self._event.title)
        return cal

    def generate_event(self):
        event = Event()
        event['uid'] = self._event.event_id
        event.add('summary', self._event.title)
        event.add('description', self._event.description)
        event.add('X-MICROSOFT-CDO-BUSYSTATUS', 'BUSY')
        event.add('dtstart', self._startdt)
        event.add('dtend', self._enddt)
        event.add('dtstamp', self._startdt)
        event['location'] = vText(self._event.location)
        return event

    def generate_organizer(self):
        organizer = vCalAddress('MAILTO:' + self._event.organizer_email)
        organizer.params['cn'] = vText(self._event.organizer_name)
        organizer.params['role'] = vText('Organizer')
        return organizer

    def generate_alarm(self):
        alarm = Alarm()
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('DESCRIPTION', self._event.description)
        alarm.add('TRIGGER', timedelta(minutes=-15))
        return alarm

    def generate_datetime(self, dts):
        dt = datetime.strptime(dts, "%Y-%m-%dT%H:%M:%SZ")
        dt.replace(tzinfo=pytz.timezone('America/New_York'))
        dtu = dt.astimezone(timezone.utc)
        return dtu
