import locale
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from .icalgenerator import iCalGenerator
import os

def generate_email(title, message_file, root='./', *args, **kwargs):
    print(os.getcwd())
    env = Environment(loader=FileSystemLoader(os.path.join(root, 'emails')))
    t = env.get_template('template.html')

    tmsg = env.get_template(message_file)
    msg = tmsg.render(kwargs)
    html = t.render(kwargs, message=msg)
    return html


def generate_email_event(event):
    event_obj = {}
    event_obj['event_id'] = event.event_id
    event_obj['title'] = event.title
    try:
        locale.setlocale(locale.LC_ALL, 'fr_CA')
    except Exception:
        pass
    start = datetime.strptime(event.start, "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(event.end, "%Y-%m-%dT%H:%M:%SZ")
    event_obj['day'] = start.strftime("%A")
    event_obj['start'] = start.strftime("%d %B %Y")
    event_obj['times'] = start.strftime("%H:%M %Z") + ' - ' + end.strftime("%H:%M %Z")
    event_obj['description'] = event.description
    event_obj['location'] = event.location
    event_obj['organizer_name'] = event.organizer_name
    return event_obj


def get_event_ical(event):
    return iCalGenerator(event).generate()
