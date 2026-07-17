# Main Agent

This project contains a **LangGraph-based AI agent** that connects to any **Model Context Protocol (MCP)** compatible server and uses the tools exposed by that server to answer user requests.

Unlike traditional AI agents where every tool must be manually defined, this agent **automatically discovers tools** from the connected MCP server during startup. As long as a server follows the MCP specification, the agent can use it without requiring any code changes.

---
# Features

* LangGraph-based conversational agent
* Uses Groq LLM for reasoning
* Automatic MCP tool discovery
* Dynamic tool execution
* Supports multiple MCP servers simultaneously
* Works with any MCP-compatible server
* Easily extendable by adding new MCP servers
* Minimal configuration using environment variables

---

# Environment Variables

Create a `.env` file inside the project.

```env
GROQ_API_KEY=

GMAIL_MCP_PYTHON=
GMAIL_MCP_SERVER=

CALENDAR_MCP_PYTHON=
CALENDAR_MCP_SERVER=
```

## GROQ_API_KEY

Your Groq API key used by the LangGraph agent.

Example

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
```

---

## GMAIL_MCP_PYTHON

Path to the Python executable used to start the Gmail MCP Server.

Example

```env
GMAIL_MCP_PYTHON=/home/user/MCP/Gmail-MCP/venv/bin/python
```

---

## GMAIL_MCP_SERVER

Path to the Gmail MCP Server entry point.

Example

```env
GMAIL_MCP_SERVER=/home/user/MCP/Gmail-MCP/server.py
```

---

## CALENDAR_MCP_PYTHON

Path to the Python executable used to start the Calendar MCP Server.

Example

```env
CALENDAR_MCP_PYTHON=/home/user/MCP/Calendar-MCP/venv/bin/python
```

---

## CALENDAR_MCP_SERVER

Path to the Calendar MCP Server entry point.

Example

```env
CALENDAR_MCP_SERVER=/home/user/MCP/Calendar-MCP/server.py
```

---

# Running the Agent

After configuring the environment variables, start the agent.

```bash
python main.py
```

During startup, the agent will:

1. Load the Groq LLM.
2. Launch all configured MCP servers.
3. Connect to each server using the Model Context Protocol.
4. Discover all available tools.
5. Combine the discovered tools into a single toolset.
6. Wait for user queries.
7. Select and execute the appropriate tool based on the user's request.

---

# How It Works

```text
                   User
                     │
                     ▼
            LangGraph Workflow
                     │
                     ▼
                MCP Client
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 Gmail MCP Server        Calendar MCP Server
        │                         │
        └────────────┬────────────┘
                     ▼
         Discover Available Tools
                     │
                     ▼
          Combined Tool Collection
                     │
                     ▼
        Groq LLM Selects Appropriate Tool
                     │
                     ▼
              Execute Selected Tool
                     │
                     ▼
              Return Final Response
```

---

# Connecting MCP Servers

Configure all MCP servers inside the `.env` file.

```env
GROQ_API_KEY=gsk_your_api_key

GMAIL_MCP_PYTHON=/path/to/Gmail-MCP/venv/bin/python
GMAIL_MCP_SERVER=/path/to/Gmail-MCP/server.py

CALENDAR_MCP_PYTHON=/path/to/Calendar-MCP/venv/bin/python
CALENDAR_MCP_SERVER=/path/to/Calendar-MCP/server.py
```

Run the agent.

```bash
python main.py
```

At startup, the agent launches both MCP servers, discovers all available tools, and binds them to the language model.

Example prompts:

### Gmail

* Read my latest emails.
* Show unread emails.
* Reply to the latest email.
* Draft an email to Alice.

### Calendar

* What meetings do I have today?
* Create a meeting tomorrow at 3 PM.
* Move tomorrow's meeting to 5 PM.
* Am I free this afternoon?

The language model automatically selects the appropriate tool from either server.

---

# Adding Additional MCP Servers

This agent is designed to support multiple MCP servers.

To add another server:

1. Create or obtain an MCP-compatible server.
2. Add its Python executable and server path to your configuration.
3. Register the server in `nodes.py` inside the `MultiServerMCPClient`.
4. Restart the agent.

For example, you could add:

* Google Drive
* Google Docs
* GitHub
* Slack
* Notion
* Jira
* PostgreSQL
* Custom enterprise services

Once connected, the agent automatically discovers and uses the new tools without changing the LangGraph workflow.

---

# Dynamic Tool Discovery

The Main Agent never hardcodes tool definitions.

When the application starts:

1. Every configured MCP server is launched.
2. The agent connects to each server.
3. Each server exposes its available tools.
4. All discovered tools are combined into a unified tool collection.
5. The Groq LLM dynamically selects the appropriate tool during conversations.

Because of this design, the same LangGraph agent can work with different MCP servers without requiring changes to the agent logic.

---

# Troubleshooting

## MCP Server Does Not Start

Verify that:

* The Python executable path is correct.
* The `server.py` path is correct.
* Each MCP server starts successfully when run manually.

---

## Only Some Tools Are Available

Check that:

* All MCP servers are correctly configured.
* Each server starts without errors.
* Each server successfully registers its tools.

---

## No Tools Found

Verify that:

* The MCP servers are running.
* The paths in the `.env` file are correct.
* The MCP servers expose tools correctly.
* The agent successfully connects to every configured server.

---

## Groq Authentication Error

Ensure your `GROQ_API_KEY` is valid and active.

---

## Module Import Errors

Install all project dependencies.

```bash
pip install -r requirements.txt
```
