"""
Update Calendar Event MCP tool.
"""

from __future__ import annotations

import json

from gcalendar.client import CalendarClient

calendar = None


def get_client():
    global calendar

    if calendar is None:
        calendar = CalendarClient()

    return calendar


def update_event(
    event_id: str,
    summary: str | None = None,
    description: str | None = None,
    location: str | None = None,
    start: str | None = None,
    end: str | None = None,
    attendees: list[str] | None = None,
):
    """
    Update an existing Google Calendar event.

    Only the provided fields will be updated.
    """

    updates = {}

    if summary is not None:
        updates["summary"] = summary

    if description is not None:
        updates["description"] = description

    if location is not None:
        updates["location"] = location

    if start is not None:
        updates["start"] = {
            "dateTime": start,
        }

    if end is not None:
        updates["end"] = {
            "dateTime": end,
        }

    if attendees is not None:
        updates["attendees"] = [
            {"email": email}
            for email in attendees
        ]

    result = get_client().update_event(
        event_id=event_id,
        **updates,
    )

    return json.dumps(
        result,
        indent=2,
    )