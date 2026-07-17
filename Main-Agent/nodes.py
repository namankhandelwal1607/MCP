"""
LangGraph Nodes.

This module connects to the local Gmail and Calendar MCP Servers
and binds all exposed tools to the Groq LLM.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from config import llm

load_dotenv()

# Gmail MCP
GMAIL_MCP_PYTHON = os.getenv(
    "GMAIL_MCP_PYTHON",
    "/home/naman/BTP/MCP/Gmail-MCP/venv/bin/python",
)

GMAIL_MCP_SERVER = os.getenv(
    "GMAIL_MCP_SERVER",
    "/home/naman/BTP/MCP/Gmail-MCP/server.py",
)

# Calendar MCP
CALENDAR_MCP_PYTHON = os.getenv(
    "CALENDAR_MCP_PYTHON",
    "/home/naman/BTP/MCP/Calendar-MCP/venv/bin/python",
)

CALENDAR_MCP_SERVER = os.getenv(
    "CALENDAR_MCP_SERVER",
    "/home/naman/BTP/MCP/Calendar-MCP/server.py",
)


async def create_agent():
    """
    Creates a LangChain model bound to all tools exposed by the
    Gmail and Calendar MCP servers.
    """

    client = MultiServerMCPClient(
        {
            "gmail": {
                "command": GMAIL_MCP_PYTHON,
                "args": [GMAIL_MCP_SERVER],
                "transport": "stdio",
            },
            "calendar": {
                "command": CALENDAR_MCP_PYTHON,
                "args": [CALENDAR_MCP_SERVER],
                "transport": "stdio",
            },
        }
    )

    tools = await client.get_tools()

    print("\nLoaded MCP Tools:\n")
    for tool in tools:
        print(f"• {tool.name}")

    print()

    model = llm.bind_tools(tools)

    return model, tools