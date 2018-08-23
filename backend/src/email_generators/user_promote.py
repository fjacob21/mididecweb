from .generator import generate_email_event, generate_email, get_event_ical

class UserPromoteEmail (object):

    def __init__(self, event, server, root='./'):
        self._server = server
        self._event = event
        self._root = root

    def generate(self, user):
        event_obj = generate_email_event(self._event)
        html = generate_email(self.title, 'usereventpromote.html', user=user, server=self._server, event=event_obj, root=self._root)
        return html

    @property
    def title(self):
        return "Confirmation pour " + self._event.title

    @property
    def iCal(self):
        return get_event_ical(self._event)
