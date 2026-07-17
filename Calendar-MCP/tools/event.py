"""
Read a single calendar event.
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


def get_event(
    event_id: str,
):
    """
    Returns a calendar event using its event ID.
    """

    result = get_client().get_event(
        event_id
    )

    return json.dumps(
        result,
        indent=2,
    )