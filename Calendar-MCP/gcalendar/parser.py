"""
Utility functions for parsing Google Calendar event objects.

Responsibilities:
- Extract common event fields
- Normalize start/end date & datetime
- Convert Google Calendar event JSON into a clean dictionary
"""

from __future__ import annotations

from typing import Any


def _get_datetime(data: dict[str, Any]) -> str:
    """
    Returns either dateTime or date depending on the event type.
    """

    if not data:
        return ""

    return (
        data.get("dateTime")
        or data.get("date")
        or ""
    )


def parse_event(event: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a Google Calendar event into a clean Python dictionary.
    """

    return {
        "id": event.get("id", ""),
        "summary": event.get("summary", ""),
        "description": event.get("description", ""),
        "location": event.get("location", ""),
        "status": event.get("status", ""),
        "created": event.get("created", ""),
        "updated": event.get("updated", ""),
        "start": _get_datetime(event.get("start", {})),
        "end": _get_datetime(event.get("end", {})),
        "creator": event.get("creator", {}).get("email", ""),
        "organizer": event.get("organizer", {}).get("email", ""),
        "attendees": [
            attendee.get("email", "")
            for attendee in event.get("attendees", [])
        ],
        "html_link": event.get("htmlLink", ""),
    }


if __name__ == "__main__":

    sample_event = {
        "id": "abc123",
        "summary": "Project Meeting",
        "description": "Discuss MCP progress",
        "location": "Google Meet",
        "status": "confirmed",
        "created": "2026-07-16T10:00:00Z",
        "updated": "2026-07-16T10:30:00Z",
        "start": {
            "dateTime": "2026-07-17T14:00:00+05:30"
        },
        "end": {
            "dateTime": "2026-07-17T15:00:00+05:30"
        },
        "creator": {
            "email": "naman@gmail.com"
        },
        "organizer": {
            "email": "naman@gmail.com"
        },
        "attendees": [
            {
                "email": "alice@gmail.com"
            },
            {
                "email": "bob@gmail.com"
            }
        ],
        "htmlLink": "https://calendar.google.com/event?eid=abc123",
    }

    parsed = parse_event(sample_event)

    print("\nParsed Event\n")

    for key, value in parsed.items():
        print(f"{key:12}: {value}")