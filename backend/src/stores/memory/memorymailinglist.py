
class MemoryMalingList():

    def __init__(self):
        self._members = []

    def add(self, user_id):
        member = {'user_id': user_id}
        self._members.append(member)

    def get_all(self):
        members = []
        for member in self._members:
            members.append(member)
        return members

    def delete(self, user_id):
        idx = self.index(user_id)
        if idx != -1:
            del self._members[idx]

    def reset(self):
        self._members = []

    def clean(self):
        self.reset()

    def index(self, user_id):
        i = 0
        for member in self._members:
            if member['user_id'] == user_id:
                return i
            i += 1
        return -1
