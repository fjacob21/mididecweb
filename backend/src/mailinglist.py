
class MailingList():

    def __init__(self):
        self._members = []

    @property
    def members(self):
        return self._members

    def register(self, member):
        if self.find_member(member.email):
            self._members.append(member)

    def unregister(self, email):
        idx = self.find_member(email)
        if idx != -1:
            del self._members[idx]

    def find_member(self, email):
        for i in range(len(self._members)):
            if self._members[i].email == email:
                return i
        return -1
