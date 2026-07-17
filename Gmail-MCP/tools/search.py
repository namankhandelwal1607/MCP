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


def search_emails(
    query: str,
    limit: int = 5,
):
    result = get_client().search_emails(
        query=query,
        limit=limit,
    )

    return json.dumps(result, indent=2)