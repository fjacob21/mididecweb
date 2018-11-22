from user import User


class Attendee():

    def __init__(self, store, user_id, event_id, static_data=None):
        self._store = store
        self._user_id = user_id
        self._user = User(self._store, self._user_id)
        self._event_id = event_id
        self._static_data = static_data

    def get_data(self):
        if self._static_data:
            return self._static_data
        return self._store.attendees.get(self._user_id, self._event_id)
    
    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._user.email

    @property
    def name(self):
        return self._user.name

    @property
    def alias(self):
        return self._user.alias

    @property
    def phone(self):
        return self._user.phone

    @property
    def useemail(self):
        return self._user.useemail

    @property
    def usesms(self):
        return self._user.usesms

    @property
    def profile(self):
        return self._user.profile

    @property
    def access(self):
        return self._user.access

    @property
    def is_normal_user(self):
        return self._user.is_normal_user

    @property
    def is_manager(self):
        return self._user.is_manager

    @property
    def is_super_user(self):
        return self._user.is_super_user

    @property
    def validated(self):
        return self._user.validated

    @property
    def smsvalidated(self):
        return self._user.smsvalidated

    @property
    def lastlogin(self):
        return self._user.lastlogin

    @property
    def loginkey(self):
        return self._user.loginkey

    @property
    def avatar_path(self):
        return self._user.avatar_path

    @property
    def create_date(self):
        return self._user.create_date

    @property
    def smscode(self):
        return self._user.smscode
    
    @property
    def present(self):
        return self.get_data()['present']
    
    @property
    def present_time(self):
        return self.get_data()['present_time']

    def __eq__(self, value):
        return self.get_data() == value.get_data()

