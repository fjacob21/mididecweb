import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logger

class EmailSender():

    def __init__(self, usr, psw, users, email, server='smtp.gmail.com'):
        self._server = server
        self._psw = psw
        self._from = usr
        self._users = users
        self._email = email

    def send(self):
        res = True
        for user in self._users:
            res = res and self.send_user(user)
        return res

    def send_user(self, user):
        fromaddr = self._from
        toaddr = user.email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = self._email.title

        body = self._email.generate(user)
        ical = self._email.iCal
        msg.attach(MIMEText(body, 'html'))
        if ical:
            icalmsg = MIMEText(ical, 'plain')
            icalmsg.add_header('Content-Disposition', 'attachment', filename='event.ics')
            msg.attach(icalmsg)

        try:
            server = smtplib.SMTP(self._server, 587)
            server.starttls()
            server.login(fromaddr, self._psw)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            logger.get().info('Send email user:{0} email:{1}'.format(user.user_id, toaddr))
            return True
        except Exception as e:
            print(e)
            logger.get().error('Send email user:{0} email:{1} ex:{2}'.format(user.user_id, toaddr, e))
            return False
