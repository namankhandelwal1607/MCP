# from gmail.client import GmailClient

# gmail = GmailClient()

from gmail.client import GmailClient
import json
gmail = None

def get_client():
    global gmail

    if gmail is None:
        gmail = GmailClient()

    return gmail

def reply_email(
    thread_id: str,
    to: str,
    subject: str,
    body: str,
):
    result = get_client().reply_email(
        thread_id,
        to,
        subject,
        body,
    )
    return json.dumps(result, indent=2)