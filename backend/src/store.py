import sqlite3
from events import Events
from event import Event
from attendee import Attendee
from mailinglist import MailingList
from mailinglist_member import MailingListMember
from datetime import datetime, timedelta
import pytz


class Store():

    def __init__(self, db='mididec.db'):
        self._db = db
        self._conn = None

    def connect(self):
        self._conn = sqlite3.connect(self._db)

    def close(self):
        self._conn.close()
        self._conn = None

    def store_events(self, events):
        if not self._conn:
            self.connect()
        self.drop_events()
        self.create_events()
        for ev in events.list:
            self.insert_event(ev)
            for a in ev.attendees:
                self.insert_attendee(ev.uid, a)
            for a in ev.waiting_attendees:
                self.insert_waitings_attendee(ev.uid, a)

    def store_mailinglist(self, mailinglist):
        if not self._conn:
            self.connect()
        self.drop_mailinglist()
        self.create_mailinglist()
        for m in mailinglist.members:
            self.insert_member(m)

    def restore_events(self):
        if not self._conn:
            self.connect()
        events = Events()
        evs = self.fetch_events()
        for ev in evs:
            event = self.restore_event(ev)
            events.add(event)
            attendees = self.fetch_attendees(event.uid)
            for a in attendees:
                attendee = self.restore_attendee(a)
                event.register_attendee(attendee)
            waiting_attendees = self.fetch_waitings_attendee(event.uid)
            for a in waiting_attendees:
                attendee = self.restore_attendee(a)
                event.register_attendee(attendee)
        return events

    def restore_mailinglist(self):
        if not self._conn:
            self.connect()
        ml = MailingList()
        members = self.fetch_members()
        for m in members:
            member = self.restore_member(m)
            ml.register(member)
        return ml

    def fetch_events(self):
        try:
            r = self._conn.execute("select * from event")
            res = r.fetchall()
            return res
        except Exception as e:
            return []

    def fetch_attendees(self, uid):
        t = (uid,)
        try:
            r = self._conn.execute('SELECT * FROM attendee WHERE evenduid=?', t)
            return r.fetchall()
        except Exception as e:
            print(e)
            return []

    def fetch_waitings_attendee(self, uid):
        t = (uid,)
        try:
            r = self._conn.execute('SELECT * FROM waitings_attendee WHERE evenduid=?', t)
            return r.fetchall()
        except Exception:
            return []

    def fetch_members(self):
        try:
            r = self._conn.execute('SELECT * FROM mailinglist')
            return r.fetchall()
        except Exception:
            return []

    def restore_member(self, m):
        member = MailingListMember(m[0], m[1], m[2], bool(m[3]), bool(m[4]))
        return member

    def restore_event(self, ev):
        start = self.generate_datetime(ev[4])
        dur = timedelta(seconds=float(ev[5]))
        event = Event(ev[1], ev[2], int(ev[3]), start, dur, ev[6], ev[7], ev[8], ev[0])
        return event

    def restore_attendee(self, a):
        attendee = Attendee(a[1], a[2], a[3], bool(a[4]), bool(a[5]))
        return attendee

    def insert_event(self, event):
        sql = "insert into event VALUES ("
        sql += '"' + event.uid + '", '
        sql += '"' + event.title + '", '
        sql += '"' + event.description + '", '
        sql += '"' + str(event.max_attendee) + '", '
        sql += '"' + event.start + '", '
        sql += '"' + str(event.duration) + '", '
        sql += '"' + event.location + '", '
        sql += '"' + event.organizer_name + '", '
        sql += '"' + event.organizer_email + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def insert_attendee(self, uid, attendee):
        sql = "insert into attendee VALUES ("
        sql += '"' + uid + '", '
        sql += '"' + attendee.name + '", '
        sql += '"' + attendee.email + '", '
        sql += '"' + attendee.phone + '", '
        sql += '"' + str(attendee.sendremindemail) + '", '
        sql += '"' + str(attendee.sendremindsms) + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def insert_waitings_attendee(self, uid, attendee):
        sql = "insert into waitings_attendee VALUES ("
        sql += '"' + uid + '", '
        sql += '"' + attendee.name + '", '
        sql += '"' + attendee.email + '", '
        sql += '"' + attendee.phone + '", '
        sql += '"' + str(attendee.sendremindemail) + '", '
        sql += '"' + str(attendee.sendremindsms) + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def insert_member(self, member):
        sql = "insert into mailinglist VALUES ("
        sql += '"' + member.name + '", '
        sql += '"' + member.email + '", '
        sql += '"' + member.phone + '", '
        sql += '"' + str(member.useemail) + '", '
        sql += '"' + str(member.usesms) + '") '
        self._conn.execute(sql)
        self._conn.commit()

    def drop_events(self):
        try:
            self._conn.execute("DROP TABLE event")
            self._conn.execute("DROP TABLE attendee")
            self._conn.execute("DROP TABLE waitings_attendee")
            self._conn.commit()
        except Exception:
            pass

    def drop_mailinglist(self):
        try:
            self._conn.execute("DROP TABLE mailinglist")
            self._conn.commit()
        except Exception:
            pass

    def create_events(self):
        self._conn.execute("create table event(uid, title, description, max_attendee, start, duration, location, organizer_name, organizer_email)")
        self._conn.execute("create table attendee(evenduid, name, email, phone, sendremindemail, sendremindsms)")
        self._conn.execute("create table waitings_attendee(evenduid, name, email, phone, sendremindemail, sendremindsms)")
        self._conn.commit()

    def create_mailinglist(self):
        self._conn.execute("create table mailinglist(name, email, phone, useemail, usesms)")
        self._conn.commit()

    def generate_datetime(self, date):
        dt = datetime.strptime(date,
                               "%Y-%m-%dT%H:%M:%SZ")
        dat = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
                       tzinfo=pytz.timezone("America/New_York"))
        return dat
