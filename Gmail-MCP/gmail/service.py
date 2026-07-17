from __future__ import annotations

import logging

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from .auth import get_credentials

logger = logging.getLogger(__name__)


def get_gmail_service() -> Resource:
    try:

        logger.info("Creating Gmail service...")

        creds = get_credentials()

        service = build(
            "gmail",
            "v1",
            credentials=creds,
            cache_discovery=False,
        )

        logger.info("Gmail service created successfully.")

        return service

    except HttpError:
        logger.exception("Unable to create Gmail service.")
        raise