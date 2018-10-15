from mock import patch, Mock, call

from deaddrop import get_task_and_notes, send_maildrop


def test__get_task_and_notes__returns_task_string_and_notes_string():
    task_and_notes_string = 'Train for World Cup ,, This might take awhile...'
    task, notes = get_task_and_notes(task_and_notes_string, ',,')
    assert task == 'Train for World Cup'
    assert notes == 'This might take awhile...'

def test__get_task_and_notes__when__no_space_between_task_and_notes__returns_task_string_and_notes_string():
    task_and_notes_string = 'Train for World Cup,,This might take awhile...'
    task, notes = get_task_and_notes(task_and_notes_string, ',,')
    assert task == 'Train for World Cup'
    assert notes == 'This might take awhile...'


@patch('deaddrop.smtplib')
def test__send_maildrop__calls_sendmail_method_on_smtp_server_with_from_to_subject_and_body(mock_smtplib):
    mock_smtp_server = Mock()
    mock_smtplib.SMTP_SSL.return_value = mock_smtp_server

    send_maildrop(
        from_addr='foo@barmail.baz',
        to_addr='a@bmail.c',
        subject='This is the task content',
        body='this is the notes content',
    )

    expected_email_text = 'From: foo@barmail.baz\nTo: a@bmail.c\nSubject: This is the task content\n\nthis is the notes content\n'

    expected_call = call('foo@barmail.baz', ['a@bmail.c'], expected_email_text)

    mock_smtp_server.sendmail.assert_has_calls([expected_call])
