from .generator import generate_email_event, generate_email

class EventPublishEmail (object):

    def __init__(self, event, server, root='./'):
        self._server = server
        self._event = event
        self._root = root

    def generate(self, user):
        event_obj = generate_email_event(self._event)
        html = generate_email(self.title, 'eventpub.html', server=self._server, event=event_obj, user=user, root=self._root)
        return html

    @property
    def title(self):
        return "Nouvelle rencontre"

    @property
    def iCal(self):
        return ''
