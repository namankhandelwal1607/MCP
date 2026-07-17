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

def send_email(
    to: str,
    subject: str,
    body: str,
):
    result = get_client().send_email(
        to,
        subject,
        body,
    )

    return json.dumps(result, indent=2)