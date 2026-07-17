"""
Utility functions for parsing Gmail API message objects.

Responsibilities:
- Extract common email headers
- Decode Base64 encoded bodies
- Handle multipart MIME messages
- Convert Gmail message JSON into a clean dictionary
"""

from __future__ import annotations

import base64
from typing import Any


def get_header(headers: list[dict[str, Any]], name: str) -> str:
    """
    Returns the value of a specific email header.

    Args:
        headers: List of Gmail message headers.
        name: Header name to search for.

    Returns:
        Header value if found, otherwise an empty string.
    """
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")

    return ""


def decode_base64(data: str) -> str:
    """
    Decode Gmail URL-safe Base64 encoded string.

    Args:
        data: Encoded string.

    Returns:
        Decoded UTF-8 string.
    """
    if not data:
        return ""

    padding = "=" * (-len(data) % 4)

    try:
        decoded = base64.urlsafe_b64decode(data + padding)
        return decoded.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def extract_body(payload: dict[str, Any]) -> str:
    """
    Recursively extracts the plain-text body from a Gmail message.
    """

    if "parts" in payload:

        for part in payload["parts"]:

            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":

                data = part.get("body", {}).get("data")

                if data:
                    return decode_base64(data)

            body = extract_body(part)

            if body:
                return body

    data = payload.get("body", {}).get("data")

    if data:
        return decode_base64(data)

    return ""


def parse_message(message: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a Gmail API message into a clean Python dictionary.
    """

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    return {
        "id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
        "snippet": message.get("snippet", ""),
        "from": get_header(headers, "From"),
        "to": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "body": extract_body(payload),
    }


if __name__ == "__main__":

    sample_message = {
        "id": "123456789",
        "threadId": "thread123",
        "snippet": "Hello Naman...",
        "payload": {
            "headers": [
                {
                    "name": "From",
                    "value": "OpenAI <noreply@openai.com>"
                },
                {
                    "name": "To",
                    "value": "naman@gmail.com"
                },
                {
                    "name": "Subject",
                    "value": "Welcome to Gmail MCP"
                },
                {
                    "name": "Date",
                    "value": "Mon, 14 Jul 2026 12:30:00 +0530"
                }
            ],
            "body": {
                "data": "SGVsbG8gTmFtYW4hCldlbGNvbWUgdG8gR21haWwgTUNQLg=="
            }
        }
    }

    parsed = parse_message(sample_message)

    print("\nParsed Email\n")

    for key, value in parsed.items():
        print(f"{key:10}: {value}")