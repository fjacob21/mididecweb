# from datetime import datetime, timedelta
# import pytz
# from src.event import Event
# from src.eventtextgenerator import EventTextGenerator
#
#
# def generate_event():
#     start = datetime.now(pytz.timezone("America/New_York"))
#     dur = timedelta(hours=1)
#     return Event("test", "test", 20, start, dur, 'test', 'test', 'fjacob21@hotmail.com', 'test')
#
#
# def test_generate_event_text_short():
#     e = generate_event()
#     gen = EventTextGenerator(e)
#     text = gen.generate()
#     assert text
#     assert type(text) == str
#
#
# def test_generate_event_text_long():
#     e = generate_event()
#     gen = EventTextGenerator(e, False)
#     text = gen.generate()
#     assert text
#     assert type(text) == str
