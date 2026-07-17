"""
Delete Calendar Event MCP tool.
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


def delete_event(
    event_id: str,
):
    """
    Delete a Google Calendar event.
    """

    result = get_client().delete_event(
        event_id=event_id,
    )

    return json.dumps(
        result,
        indent=2,
    )