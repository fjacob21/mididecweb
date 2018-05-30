from twilio.rest import Client


class SmsSender():

    def __init__(self, sid, token, to, title, body, fromphone='+15146003703'):
        self._from = fromphone
        self._sid = sid
        self._token = token
        self._to = to
        self._title = title
        self._body = body

    def send(self):
        try:
            client = Client(self._sid, self._token)

            client.api.account.messages.create(
                to=self._to,
                from_="+15799140888",
                body=self._body,
                messaging_service_sid='MGed4b41125820097ff0c3e49272cf53a1')
            return True
        except Exception:
            return False
