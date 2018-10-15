import os
import smtplib

import click


OMNIFOCUS_MAILDROP_ADDRESS = os.environ.get('DD_OMNIFOCUS_MAILDROP_ADDRESS')
SENDER_EMAIL = os.environ.get('DD_SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('DD_SENDER_PASSWORD')
NOTES_DELIMITER = os.environ.get('DD_NOTES_DELIMITER', ',,')


@click.command()
@click.argument('task', nargs=-1)
def send_task_to_maildrop(task):
    task_and_notes_string = ' '.join(task)
    task, notes = get_task_and_notes(task_and_notes_string, NOTES_DELIMITER)

    send_maildrop(
        from_addr=SENDER_EMAIL,
        to_addr=OMNIFOCUS_MAILDROP_ADDRESS,
        subject=task,
        body=notes,
    )
    click.echo('Your task has been sent to OmniFocus.')


def send_maildrop(from_addr, to_addr, subject, body):

    email_text = """\
From: {from_addr}
To: {to_addr}
Subject: {subject}

{body}
""".format(from_addr=from_addr, to_addr=", ".join([to_addr]), subject=subject, body=body)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(from_addr, SENDER_PASSWORD)
    server.sendmail(from_addr, [to_addr], email_text)
    server.close()


def get_task_and_notes(task_and_notes, delimiter):
    task, notes = task_and_notes.split(delimiter)
    return task.strip(), notes.strip()


if __name__ == '__main__':
    send_task_to_maildrop()
