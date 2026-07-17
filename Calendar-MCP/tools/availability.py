"""
Check Calendar Availability MCP tool.
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


def check_availability(
    start: str,
    end: str,
):
    """
    Check whether the user is free during a given time range.
    """

    result = get_client().check_free_busy(
        start=start,
        end=end,
    )

    return json.dumps(
        result,
        indent=2,
    )