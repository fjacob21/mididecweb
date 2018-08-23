from .generator import generate_email_event, generate_email, get_event_ical

class EventDateChangedEmail (object):

    def __init__(self, event, old_event, server, root='./'):
        self._server = server
        self._event = event
        self._old_event = old_event
        self._root = root

    def generate(self, user):
        event_obj = generate_email_event(self._event)
        old_event_obj = generate_email_event(self._old_event)
        html = generate_email(self.title, 'eventchdate.html', server=self._server, event=event_obj, old_event=old_event_obj, user=user, root=self._root)
        return html

    @property
    def title(self):
        return "Date de l'évènement est changée"

    @property
    def iCal(self):
        return get_event_ical(self._event)
