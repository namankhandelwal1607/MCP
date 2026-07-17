"""
Read Calendar MCP tools.
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


def list_upcoming_events(
    limit: int = 10,
):
    """
    Returns upcoming calendar events.
    """

    result = get_client().list_upcoming_events(limit)

    return json.dumps(
        result,
        indent=2,
    )


def list_calendars():
    """
    Returns all calendars.
    """

    result = get_client().list_calendars()

    return json.dumps(
        result,
        indent=2,
    )