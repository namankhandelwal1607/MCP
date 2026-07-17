"""
Read a single email.
"""

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

def read_email_by_id(
    email_id: str,
):
    result=  get_client().read_email_by_id(email_id)
    return json.dumps(result, indent=2)