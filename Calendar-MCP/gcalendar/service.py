from __future__ import annotations

import logging

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from .auth import get_credentials

logger = logging.getLogger(__name__)


def get_calendar_service() -> Resource:
    """
    Create and return an authenticated Google Calendar service.
    """

    try:
        logger.info("Creating Google Calendar service...")

        creds = get_credentials()

        service = build(
            "calendar",
            "v3",
            credentials=creds,
            cache_discovery=False,
        )

        logger.info("Google Calendar service created successfully.")

        return service

    except HttpError:
        logger.exception("Unable to create Google Calendar service.")
        raise