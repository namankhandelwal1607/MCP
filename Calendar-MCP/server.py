"""
Local Google Calendar MCP Server.

This server exposes Google Calendar functionality as MCP tools.

Current Tools:
- list_upcoming_events
- list_calendars
- get_event
- create_event
- update_event
- delete_event
- search_events
- check_availability
"""

from __future__ import annotations

import logging

from fastmcp import FastMCP

from tools.read import (
    list_upcoming_events,
    list_calendars,
)
from tools.event import get_event
from tools.create import create_event
from tools.update import update_event
from tools.delete import delete_event
from tools.search import search_events
from tools.availability import check_availability

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Google Calendar MCP Server",
)


# ============================================================
# Read Tools
# ============================================================

@mcp.tool(
    name="list_upcoming_events",
    description="List upcoming events from the user's Google Calendar.",
)
def upcoming_events(
    limit: int = 10,
):
    logger.info("MCP Tool Invoked: list_upcoming_events")

    return list_upcoming_events(limit)


@mcp.tool(
    name="list_calendars",
    description="List all Google Calendars available to the user.",
)
def calendars():
    logger.info("MCP Tool Invoked: list_calendars")

    return list_calendars()


@mcp.tool(
    name="get_event",
    description="Read a Google Calendar event using its event ID.",
)
def read_event(
    event_id: str,
):
    logger.info("MCP Tool Invoked: get_event")

    return get_event(event_id)


# ============================================================
# Create
# ============================================================

@mcp.tool(
    name="create_event",
    description="Create a new Google Calendar event.",
)
def create_event_tool(
    summary: str,
    start: str,
    end: str,
    description: str = "",
    location: str = "",
    attendees: list[str] | None = None,
):
    logger.info("MCP Tool Invoked: create_event")

    return create_event(
        summary=summary,
        start=start,
        end=end,
        description=description,
        location=location,
        attendees=attendees,
    )


# ============================================================
# Update
# ============================================================

@mcp.tool(
    name="update_event",
    description="Update an existing Google Calendar event.",
)
def update_event_tool(
    event_id: str,
    summary: str | None = None,
    description: str | None = None,
    location: str | None = None,
    start: str | None = None,
    end: str | None = None,
    attendees: list[str] | None = None,
):
    logger.info("MCP Tool Invoked: update_event")

    return update_event(
        event_id=event_id,
        summary=summary,
        description=description,
        location=location,
        start=start,
        end=end,
        attendees=attendees,
    )


# ============================================================
# Delete
# ============================================================

@mcp.tool(
    name="delete_event",
    description="Delete a Google Calendar event.",
)
def delete_event_tool(
    event_id: str,
):
    logger.info("MCP Tool Invoked: delete_event")

    return delete_event(event_id)


# ============================================================
# Search
# ============================================================

@mcp.tool(
    name="search_events",
    description="Search Google Calendar events using a keyword.",
)
def search_events_tool(
    query: str,
    limit: int = 10,
):
    logger.info("MCP Tool Invoked: search_events")

    return search_events(
        query=query,
        limit=limit,
    )


# ============================================================
# Availability
# ============================================================

@mcp.tool(
    name="check_availability",
    description="Check whether the user's calendar is free during a specified time range.",
)
def availability_tool(
    start: str,
    end: str,
):
    logger.info("MCP Tool Invoked: check_availability")

    return check_availability(
        start=start,
        end=end,
    )


if __name__ == "__main__":

    logger.info("Starting Google Calendar MCP Server...")

    mcp.run()