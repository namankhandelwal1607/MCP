"""
Read email MCP tools.
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


def read_latest_emails(limit: int = 5):

    result = get_client().read_latest_emails(limit)
    return json.dumps(result, indent=2)


def read_unread_emails(limit: int = 5):

    result = get_client().read_unread_emails(limit)
    return json.dumps(result, indent=2)