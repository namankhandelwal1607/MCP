"""
Create Calendar Event MCP tool.
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


def create_event(
    summary: str,
    start: str,
    end: str,
    description: str = "",
    location: str = "",
    attendees: list[str] | None = None,
):
    """
    Create a new Google Calendar event.
    """

    result = get_client().create_event(
        summary=summary,
        start=start,
        end=end,
        description=description,
        location=location,
        attendees=attendees,
    )

    return json.dumps(
        result,
        indent=2,
    )