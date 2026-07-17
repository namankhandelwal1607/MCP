"""
High-level Google Calendar client.

Encapsulates all Calendar API operations.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from googleapiclient.errors import HttpError

from .parser import parse_event
from .service import get_calendar_service

logger = logging.getLogger(__name__)


class CalendarClient:
    """
    High-level wrapper around the Google Calendar API.
    """

    def __init__(self):
        self.service = get_calendar_service()

    # ============================================================
    # Private Helpers
    # ============================================================

    def _get_event(
        self,
        event_id: str,
        calendar_id: str = "primary",
    ) -> dict[str, Any]:
        """
        Fetch a single event.
        """

        return (
            self.service.events()
            .get(
                calendarId=calendar_id,
                eventId=event_id,
            )
            .execute()
        )

    def _list_events(
        self,
        calendar_id: str = "primary",
        max_results: int = 10,
        time_min: str | None = None,
        query: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch events from Google Calendar.
        """

        if time_min is None:
            time_min = (
                datetime.now(timezone.utc)
                .isoformat()
            )

        response = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                q=query,
            )
            .execute()
        )

        events = response.get("items", [])

        return [
            parse_event(event)
            for event in events
        ]

    # ============================================================
    # Public APIs
    # ============================================================

    def list_upcoming_events(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Returns upcoming events.
        """

        return self._list_events(
            max_results=limit,
        )

    def search_events(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search calendar events.
        """

        return self._list_events(
            max_results=limit,
            query=query,
        )

    def get_event(
        self,
        event_id: str,
    ) -> dict[str, Any]:
        """
        Read one event.
        """

        event = self._get_event(event_id)

        return parse_event(event)

    def list_calendars(
        self,
    ) -> list[dict[str, Any]]:
        """
        Returns all calendars.
        """

        response = (
            self.service.calendarList()
            .list()
            .execute()
        )

        calendars = []

        for cal in response.get("items", []):

            calendars.append(
                {
                    "id": cal.get("id"),
                    "summary": cal.get("summary"),
                    "primary": cal.get("primary", False),
                    "timeZone": cal.get("timeZone"),
                }
            )

        return calendars

    # ============================================================
    # CRUD Operations
    # ============================================================

    def create_event(
        self,
        summary: str,
        start: str,
        end: str,
        description: str = "",
        location: str = "",
        attendees: list[str] | None = None,
        calendar_id: str = "primary",
    ) -> dict[str, Any]:

        body = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {
                "dateTime": start,
            },
            "end": {
                "dateTime": end,
            },
        }

        if attendees:
            body["attendees"] = [
                {"email": email}
                for email in attendees
            ]

        event = (
            self.service.events()
            .insert(
                calendarId=calendar_id,
                body=body,
            )
            .execute()
        )

        return parse_event(event)

    def update_event(
        self,
        event_id: str,
        **updates,
    ) -> dict[str, Any]:
        """
        Update any event fields.
        """

        event = self._get_event(event_id)

        event.update(updates)

        updated = (
            self.service.events()
            .update(
                calendarId="primary",
                eventId=event_id,
                body=event,
            )
            .execute()
        )

        return parse_event(updated)

    def delete_event(
        self,
        event_id: str,
    ) -> dict[str, str]:
        """
        Delete an event.
        """

        self.service.events().delete(
            calendarId="primary",
            eventId=event_id,
        ).execute()

        return {
            "status": "success",
            "message": "Event deleted successfully.",
        }
    
    def check_free_busy(
        self,
        start: str,
        end: str,
        calendar_id: str = "primary",
    ):
        """
        Check whether the calendar is free during a given time range.
        """

        body = {
            "timeMin": start,
            "timeMax": end,
            "items": [
                {
                    "id": calendar_id,
                }
            ],
        }

        response = (
            self.service.freebusy()
            .query(body=body)
            .execute()
        )

        busy = (
            response["calendars"]
            .get(calendar_id, {})
            .get("busy", [])
        )

        return {
            "available": len(busy) == 0,
            "busy_slots": busy,
        }