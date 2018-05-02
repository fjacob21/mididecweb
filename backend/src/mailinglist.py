from user import User


class MailingList():

    def __init__(self, store):
        self._store = store

    @property
    def members(self):
        result = []
        members = self._store.mailinglist.get_all()
        for member in members:
            print('User', member['user_id'])
            result.append(User(self._store, member['user_id']))
        return result

    def register(self, user):
        if self.find_member(user.email):
            self._store.mailinglist.add(user.user_id)

    def unregister(self, email):
        idx = self.find_member(email)
        if idx != -1:
            return self._store.mailinglist.delete(self.members[idx].user_id)
        return False

    def find_member(self, email):
        for i in range(len(self.members)):
            if self.members[i].email == email:
                return i
        return -1
