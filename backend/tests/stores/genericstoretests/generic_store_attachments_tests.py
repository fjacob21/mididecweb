
def test_attachments(attachments):
    attachments.add('path', 'event')
    assert len(attachments.get_all('event')) == 1
    attendee = attachments.get_all('event')[0]
    assert attendee
    assert attendee['path'] == 'path'
    assert attendee['event_id'] == 'event'
    attachments.delete('path', 'path')
    attachments.delete('path', 'path')

    attachments.add('path', 'event')
    attachments.reset()
    assert len(attachments.get_all('event')) == 0
    attachments.reset()

    attachments.add('path', 'event')
    attachments.clean()
    assert len(attachments.get_all('event')) == 0
    attachments.clean()
