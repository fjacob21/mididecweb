from .generator import generate_email


class UserResetPasswordEmail (object):

    def __init__(self, request_id, server, root='./'):
        self._server = server
        self._request_id = request_id
        self._root = root
        print('reset', server)

    def generate(self, user):
        html = generate_email(self.title, 'userresetpassword.html',
                              server=self._server, user=user,
                              request_id=self._request_id, root=self._root)
        return html

    @property
    def title(self):
        return "Reset password"

    @property
    def iCal(self):
        return ''
