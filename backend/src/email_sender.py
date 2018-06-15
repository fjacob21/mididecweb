import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender():

    def __init__(self, usr, psw, to, title, body, type='plain',
                 server='smtp.gmail.com', ical=''):
        self._server = server
        self._psw = psw
        self._type = type
        self._from = usr
        self._to = to
        self._title = title
        self._body = body
        self._ical = ical

    def send(self):
        fromaddr = self._from
        toaddr = self._to
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = self._title

        body = self._body
        msg.attach(MIMEText(body, self._type))
        if self._ical:
            icalmsg = MIMEText(self._ical, 'plain')
            icalmsg.add_header('Content-Disposition', 'attachment', filename='event.ics')
            msg.attach(icalmsg)

        try:
            server = smtplib.SMTP(self._server, 587)
            server.starttls()
            server.login(fromaddr, self._psw)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False
