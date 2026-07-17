"""
Handles Gmail OAuth2 authentication.
"""

from __future__ import annotations

import logging
import os
import json

from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = PROJECT_ROOT / os.getenv(
    "GOOGLE_CREDENTIALS",
    "credentials.json",
)

TOKEN_FILE = PROJECT_ROOT / os.getenv(
    "GOOGLE_TOKEN",
    "token.json",
)


def get_credentials() -> Credentials:
    creds = None

    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_FILE),
                SCOPES,
            )

        except json.JSONDecodeError:
            logger.warning("Invalid token.json")
            creds = None

    if creds and creds.expired and creds.refresh_token:
        logger.info("Refreshing expired token...")
        creds.refresh(Request())

    elif not creds or not creds.valid:

        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {CREDENTIALS_FILE}"
            )

        logger.info("Starting OAuth flow...")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES,
        )

        creds = flow.run_local_server(
            port=0,
            open_browser=False,
        )

    TOKEN_FILE.write_text(creds.to_json())

    logger.info("Authentication successful.")

    return creds

def main() -> None:
    """
    Authenticate the user and generate token.json.
    """
    try:
        get_credentials()
        print(f"✅ Authentication successful!")
        print(f"Token saved to: {TOKEN_FILE}")

    except Exception as e:
        logger.exception("Authentication failed.")
        print(f"❌ Authentication failed: {e}")


if __name__ == "__main__":
    main()