"""
Search Calendar Events MCP tool.
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


def search_events(
    query: str,
    limit: int = 10,
):
    """
    Search Google Calendar events using a keyword.

    Args:
        query: Search keyword.
        limit: Maximum number of matching events.
    """

    result = get_client().search_events(
        query=query,
        limit=limit,
    )

    return json.dumps(
        result,
        indent=2,
    )