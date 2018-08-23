from .generator import generate_email_event, generate_email

class UserValidationEmail (object):

    def __init__(self, server, root='./'):
        self._server = server
        self._root = root

    def generate(self, user):
        html = generate_email(self.title, 'uservalidate.html', server=self._server, user=user, root=self._root)
        return html

    @property
    def title(self):
        return "Validation MidiDecouverte"

    @property
    def iCal(self):
        return ''
