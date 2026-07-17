"""
Local Gmail MCP Server.

This server exposes Gmail functionality as MCP tools.

Current Tools:
- read_latest_emails
- read_unread_emails
"""

from __future__ import annotations

import logging

from fastmcp import FastMCP

from tools.read import (
    read_latest_emails,
    read_unread_emails,
)
from tools.search import search_emails
from tools.email import read_email_by_id
from tools.send import send_email
from tools.draft import create_draft
from tools.reply import reply_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Gmail MCP Server",
)


@mcp.tool(
    name="read_latest_emails",
    description="Read the latest emails from the user's Gmail inbox.",
)
def latest_emails(limit: int = 5):
    """
    Returns the latest emails.

    Args:
        limit: Maximum number of emails to return.
    """

    logger.info("MCP Tool Invoked: read_latest_emails")

    return read_latest_emails(limit)


@mcp.tool(
    name="read_unread_emails",
    description="Read unread emails from the user's Gmail inbox.",
)
def unread_emails(limit: int = 5):
    """
    Returns unread emails.

    Args:
        limit: Maximum number of unread emails.
    """

    logger.info("MCP Tool Invoked: read_unread_emails")

    return read_unread_emails(limit)

@mcp.tool(
    name="search_emails",
    description="Search Gmail using Gmail search operators.",
)
def gmail_search(
    query: str,
    limit: int = 5,
):
    return search_emails(
        query=query,
        limit=limit,
    )

@mcp.tool(
    name="read_email_by_id",
    description="Read a complete email using its Gmail message ID.",
)
def gmail_read_email(
    email_id: str,
):
    return read_email_by_id(email_id)


@mcp.tool(
    name="send_email",
    description="Send an email to one or more recipients using the user's Gmail account.",
)
def send_email_tool(
    to: str,
    subject: str,
    body: str,
):
    """
    Sends an email.

    Args:
        to: Recipient email address(es). Multiple addresses should be comma-separated.
        subject: Subject line of the email.
        body: Plain text body of the email.
    """

    logger.info("MCP Tool Invoked: send_email")

    return send_email(
        to,
        subject,
        body,
    )


@mcp.tool(
    name="create_draft",
    description="Create a draft email in the user's Gmail account without sending it.",
)
def create_draft_tool(
    to: str,
    subject: str,
    body: str,
):
    """
    Creates a Gmail draft.

    Args:
        to: Recipient email address(es).
        subject: Subject line of the draft.
        body: Plain text body of the draft.
    """

    logger.info("MCP Tool Invoked: create_draft")

    return create_draft(
        to,
        subject,
        body,
    )


@mcp.tool(
    name="reply_email",
    description="Reply to an existing Gmail conversation using the thread ID.",
)
def reply_email_tool(
    thread_id: str,
    to: str,
    subject: str,
    body: str,
):
    """
    Replies to an existing email thread.

    Args:
        thread_id: Gmail thread ID of the conversation.
        to: Recipient email address.
        subject: Subject of the reply.
        body: Plain text reply message.
    """

    logger.info("MCP Tool Invoked: reply_email")

    return reply_email(
        thread_id,
        to,
        subject,
        body,
    )


if __name__ == "__main__":

    logger.info("Starting Gmail MCP Server...")

    mcp.run()