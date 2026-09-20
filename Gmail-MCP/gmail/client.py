"""
High-level Gmail client.

Encapsulates Gmail API operations.
"""

from __future__ import annotations

import base64
import logging
from email.mime.text import MIMEText
from typing import Any

from googleapiclient.errors import HttpError

from .parser import parse_message
from .service import get_gmail_service

logger = logging.getLogger(__name__)


class GmailClient:
    """
    High-level wrapper around the Gmail API.
    """

    def __init__(self):
        self.service = get_gmail_service()

    # ============================================================
    # Private Helpers
    # ============================================================

    def _create_message(
        self,
        to: str,
        subject: str,
        body: str,
        reply_to: str | None = None,
        in_reply_to: str | None = None,
        references: str | None = None,
    ) -> dict[str, str]:
        """
        Creates a MIME email and encodes it for the Gmail API.

        The From header is intentionally not set.
        Gmail API sends the message using the authenticated account.
        """

        import re
        from email.mime.multipart import MIMEMultipart

        is_html = "<html" in body.lower() or "<p" in body.lower() or "<div" in body.lower()
        has_markdown = "**" in body or ("[" in body and "](" in body)

        if is_html or has_markdown:
            message = MIMEMultipart("alternative")
            message["To"] = to
            message["Subject"] = subject

            if is_html:
                html_body = body
                plain_body = re.sub(r'<br\s*/?>', '\n', body)
                plain_body = re.sub(r'</p>', '\n\n', plain_body)
                plain_body = re.sub(r'<[^>]+>', '', plain_body).strip()
            else:
                paras = body.strip().split('\n\n')
                html_paras = []
                for p in paras:
                    p_html = p.replace('\n', '<br>')
                    p_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_html)
                    p_html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', p_html)
                    html_paras.append(f'<p>{p_html}</p>')
                html_body = '<div style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 1.6; color: #222222;">\n' + '\n'.join(html_paras) + '\n</div>'
                plain_body = body

            part_plain = MIMEText(plain_body, "plain", "utf-8")
            part_html = MIMEText(html_body, "html", "utf-8")

            message.attach(part_plain)
            message.attach(part_html)
        else:
            message = MIMEText(body, "plain", "utf-8")
            message["To"] = to
            message["Subject"] = subject

        if reply_to:
            message["Reply-To"] = reply_to

        if in_reply_to:
            message["In-Reply-To"] = in_reply_to

        if references:
            message["References"] = references

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode("utf-8")

        return {
            "raw": raw
        }

    def _build_query(
        self,
        sender: str | None = None,
        subject: str | None = None,
        unread: bool = False,
        latest: bool = False,
        has_attachment: bool = False,
        after: str | None = None,
        before: str | None = None,
        custom_query: str | None = None,
    ) -> str:
        """
        Builds a Gmail search query.
        """

        parts: list[str] = []

        if sender:
            parts.append(f"from:{sender}")

        if subject:
            parts.append(f"subject:{subject}")

        if unread:
            parts.append("is:unread")

        if latest:
            parts.append("newer_than:30d")

        if has_attachment:
            parts.append("has:attachment")

        if after:
            parts.append(f"after:{after}")

        if before:
            parts.append(f"before:{before}")

        if custom_query:
            parts.append(custom_query)

        return " ".join(parts)

    def _parse_summary(
        self,
        message: dict[str, Any],
    ) -> dict[str, Any]:

        parsed = parse_message(message)

        return {
            "id": parsed["id"],
            "thread_id": parsed["thread_id"],
            "from": parsed["from"],
            "to": parsed["to"],
            "subject": parsed["subject"],
            "date": parsed["date"],
            "snippet": parsed["snippet"],
        }

    def _get_message(
        self,
        email_id: str,
        format: str = "full",
    ) -> dict[str, Any]:

        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=email_id,
                format=format,
            )
            .execute()
        )

    def _fetch_messages(
        self,
        query: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        try:
            response = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=limit,
                )
                .execute()
            )

            messages = response.get("messages", [])

            results = []

            for msg in messages:
                full = self._get_message(msg["id"])

                results.append(
                    self._parse_summary(full)
                )

            return results

        except HttpError:
            logger.exception("Failed to fetch emails.")
            raise

    # ============================================================
    # Public APIs
    # ============================================================

    def find_emails(
        self,
        sender: str | None = None,
        subject: str | None = None,
        unread: bool = False,
        latest: bool = False,
        has_attachment: bool = False,
        after: str | None = None,
        before: str | None = None,
        custom_query: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Intelligent Gmail search.
        """

        query = self._build_query(
            sender=sender,
            subject=subject,
            unread=unread,
            latest=latest,
            has_attachment=has_attachment,
            after=after,
            before=before,
            custom_query=custom_query,
        )

        return self._fetch_messages(
            query=query,
            limit=limit,
        )

    def read_email(
        self,
        email_id: str,
    ) -> dict[str, Any]:
        """
        Read a complete email.
        """

        message = self._get_message(email_id)

        parsed = parse_message(message)

        body = parsed.get("body", "")

        if len(body) > 4000:
            body = body[:4000] + "\n\n...[truncated]..."

        parsed["body"] = body

        return parsed

    def get_thread(
        self,
        thread_id: str,
    ) -> list[dict[str, Any]]:
        """
        Returns all emails in a conversation thread.
        """

        thread = (
            self.service.users()
            .threads()
            .get(
                userId="me",
                id=thread_id,
                format="full",
            )
            .execute()
        )

        emails = []

        for message in thread.get("messages", []):
            emails.append(
                self._parse_summary(message)
            )

        return emails

    def get_profile(self) -> dict[str, Any]:
        """
        Returns the authenticated Gmail profile.
        """

        return (
            self.service.users()
            .getProfile(
                userId="me",
            )
            .execute()
        )

    def get_labels(self) -> list[dict[str, Any]]:
        """
        Returns Gmail labels.
        """

        response = (
            self.service.users()
            .labels()
            .list(
                userId="me",
            )
            .execute()
        )

        return response.get("labels", [])

    # ============================================================
    # Backward Compatibility
    # ============================================================

    def read_latest_emails(
        self,
        limit: int = 5,
    ):
        return self.find_emails(
            latest=True,
            limit=limit,
        )

    def read_unread_emails(
        self,
        limit: int = 5,
    ):
        return self.find_emails(
            unread=True,
            limit=limit,
        )

    def search_emails(
        self,
        query: str,
        limit: int = 5,
    ):
        return self.find_emails(
            custom_query=query,
            limit=limit,
        )

    def read_email_by_id(
        self,
        email_id: str,
    ):
        return self.read_email(email_id)

    # ============================================================
    # Send Email
    # ============================================================

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """
        Sends an email using the authenticated Gmail account.
        """

        message = self._create_message(
            to=to,
            subject=subject,
            body=body,
        )

        return (
            self.service.users()
            .messages()
            .send(
                userId="me",
                body=message,
            )
            .execute()
        )

    # ============================================================
    # Draft
    # ============================================================

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """
        Creates a Gmail draft.
        """

        message = self._create_message(
            to=to,
            subject=subject,
            body=body,
        )

        return (
            self.service.users()
            .drafts()
            .create(
                userId="me",
                body={
                    "message": message
                },
            )
            .execute()
        )

    # ============================================================
    # Reply
    # ============================================================

    def reply_email(
        self,
        thread_id: str,
        to: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """
        Replies to an existing Gmail thread.

        threadId is supplied to Gmail so the message belongs
        to the existing conversation.
        """

        message = self._create_message(
            to=to,
            subject=subject,
            body=body,
        )

        message["threadId"] = thread_id

        return (
            self.service.users()
            .messages()
            .send(
                userId="me",
                body=message,
            )
            .execute()
        )