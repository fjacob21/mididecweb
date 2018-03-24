import json


class Attendee():

    def __init__(self, name, email, phone, sendremindemail, sendremindsms):
        self._name = name
        self._email = email
        self._phone = phone
        self._sendremindemail = sendremindemail
        self._sendremindsms = sendremindsms

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def sendremindemail(self):
        return self._sendremindemail

    @property
    def sendremindsms(self):
        return self._sendremindsms

    @property
    def json(self):
        result = {}
        result['name'] = self.name
        result['email'] = self.email
        result['phone'] = self.phone
        result['sendremindemail'] = self.sendremindemail
        result['sendremindsms'] = self.sendremindsms

        return json.dumps(result)
