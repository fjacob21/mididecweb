from src.codec.attendee_json_encoder import AttendeeJsonEncoder
from src.attendee import Attendee
import json


def test_complete_user_json_encoder():
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    jsonobj = AttendeeJsonEncoder(a, True).encode('dict')
    assert jsonobj['name'] == "test"
    assert jsonobj['email'] == "test@test.com"
    assert jsonobj['phone'] == "1234567890"
    assert jsonobj['useemail'] is True
    assert jsonobj['usesms'] is True


def test_user_json_encoder():
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    jsonobj = AttendeeJsonEncoder(a).encode('dict')
    assert jsonobj['name'] == "test"
    assert 'email' not in jsonobj
    assert 'phone' not in jsonobj
    assert 'useemail' not in jsonobj
    assert 'usesms' not in jsonobj


def test_user_json_encoder_string():
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    strjson = AttendeeJsonEncoder(a).encode('string')
    assert type(strjson) == str
    dict = json.loads(strjson)
    assert dict['name'] == "test"
    assert 'email' not in dict
    assert 'phone' not in dict
    assert 'useemail' not in dict
    assert 'usesms' not in dict


def test_complete_user_json_encoder_string():
    a = Attendee("test", "test@test.com", '1234567890', True, True)
    strjson = AttendeeJsonEncoder(a, True).encode('string')
    assert type(strjson) == str
    dict = json.loads(strjson)
    assert dict['name'] == "test"
    assert dict['email'] == "test@test.com"
    assert dict['phone'] == "1234567890"
    assert dict['useemail'] is True
    assert dict['usesms'] is True
