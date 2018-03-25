import json


class MailingListMember():

    def __init__(self, name, email, phone='', useemail=True, usesms=False):
        self._name = name
        self._email = email
        self._phone = phone
        self._useemail = useemail
        self._usesms = usesms

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
    def useemail(self):
        return self._useemail

    @property
    def usesms(self):
        return self._usesms

    @property
    def json(self):
        result = {}
        result['name'] = self.name
        result['email'] = self.email
        result['phone'] = self.phone
        result['useemail'] = self.useemail
        result['usesms'] = self.usesms

        return json.dumps(result)
