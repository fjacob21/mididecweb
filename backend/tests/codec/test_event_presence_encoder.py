from src.codec.event_presences_pdf_encoder import EventPresencesPdfEncoder
from datetime import datetime, timedelta
import pytz
from src.events import Events
from PyPDF2 import PdfFileReader
import io
from src.stores import MemoryStore
from src.users import Users


def test_complete_event_presences_pdf_encoder():
    store = MemoryStore()
    events = Events(store)
    users = Users(store)
    start = datetime.now(pytz.timezone("America/New_York"))
    dur = timedelta(hours=1)
    a = users.add("test@test.com", 'name', 'alias', 'psw')
    e = events.add("test", "test", 30, start, dur, 'test', 'test', 'test@test.com', 'test', a)
    a.validated = True
    e.register_attendee(a)
    e.add_attachment('../test/test.txt')
    pdfobj = EventPresencesPdfEncoder(e, a, drawable_path='../frontend/res/drawables/', data_path='./data/').encode()
    pdfstream = io.BytesIO(pdfobj)
    PdfFileReader(pdfstream)
