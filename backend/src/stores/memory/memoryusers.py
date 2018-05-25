from datetime import datetime
import pytz


class MemoryUsers():

    def __init__(self):
        self._users = []

    def create(self, user_id, email, name, alias, psw, phone, useemail, usesms,
               profile, access, validated=False, smsvalidated=False, lastlogin='', loginkey='', avatar_path=''):
        if not self.get(user_id):
            obj = self.create_object(user_id, email, name, alias, psw, phone,
                                     useemail, usesms, profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path)
            self._users.append(obj)

    def get_all(self):
        return self._users

    def get(self, user_id):
        for user in self._users:
            if user['user_id'] == user_id:
                return user
        return None

    def update(self, user_id, email, name, alias, psw, phone, useemail, usesms,
               profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path):
        user = self.get(user_id)
        if user:
            obj = self.create_object(user_id, email, name, alias, psw, phone,
                                     useemail, usesms, profile, access, validated, smsvalidated, lastlogin, loginkey, avatar_path)
            self._users[self.index(user_id)] = obj

    def delete(self, user_id):
        idx = self.index(user_id)
        if idx != -1:
            del self._users[idx]

    def reset(self):
        self._users = []

    def clean(self):
        self.reset()

    def create_object(self, user_id, email, name, alias, psw, phone, useemail,
                      usesms, profile, access, validated=False, smsvalidated=False, lastlogin='', loginkey='', avatar_path='', create_date=''):
        if not create_date:
            create_date_dt = datetime.now(pytz.timezone("America/New_York"))
            create_date = create_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        user = {}
        user['user_id'] = user_id
        user['email'] = email
        user['name'] = name
        user['alias'] = alias
        user['phone'] = phone
        user['useemail'] = useemail
        user['usesms'] = usesms
        user['profile'] = profile
        user['psw'] = psw
        user['access'] = access
        user['validated'] = validated
        user['smsvalidated'] = smsvalidated
        user['lastlogin'] = lastlogin
        user['loginkey'] = loginkey
        user['avatar_path'] = avatar_path
        user['create_date'] = create_date
        return user

    def index(self, user_id):
        i = 0
        for user in self._users:
            if user['user_id'] == user_id:
                return i
            i += 1
        return -1
