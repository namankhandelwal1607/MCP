# Gmail MCP Server

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![MCP](https://img.shields.io/badge/MCP-Compatible-success)
![Gmail](https://img.shields.io/badge/Google-Gmail-red)
![OAuth2](https://img.shields.io/badge/Auth-OAuth2-green)

</p>

---

# Overview

The **Gmail MCP Server** exposes Gmail functionality through the **Model Context Protocol (MCP)**, allowing AI agents and MCP-compatible clients to interact with a Gmail account using natural language.

Instead of writing Gmail API calls manually, clients can invoke standardized MCP tools such as reading emails, searching messages, sending emails, replying to threads, and saving drafts.

This server follows the official **Model Context Protocol** specification and can be used with:

- Cursor
- Claude Desktop
- Continue.dev
- VS Code MCP Extensions
- LangGraph
- FastMCP Clients
- Custom MCP Clients

---

# Features

The Gmail MCP Server currently supports the following operations.

### Reading Emails

- Read latest emails
- Read unread emails
- Read email by ID

### Searching

- Search emails using Gmail query syntax

Examples:

- `from:john@gmail.com`
- `label:important`
- `newer_than:7d`
- `has:attachment`

### Sending

- Send emails
- Reply to existing emails
- Save draft emails

---

# Project Structure

```text
Gmail-MCP/
│
├── README.md
├── requirements.txt
├── server.py
│
├── gmail/
│   ├── __init__.py
│   ├── auth.py
│   ├── client.py
│   ├── parser.py
│   └── service.py
│
├── tools/
│   ├── read.py
│   ├── search.py
│   ├── email.py
│   ├── send.py
│   ├── reply.py
│   └── draft.py
│
├── credentials.json
├── token.json
│
└── venv/
```

---

# Directory Explanation

## `server.py`

Entry point of the MCP server.

Registers all available Gmail tools and starts the MCP server.

---

## `gmail/`

Contains Gmail API helper modules.

### auth.py

Handles Google OAuth authentication.

### client.py

Creates authenticated Gmail client.

### parser.py

Parses Gmail API responses into cleaner Python objects.

### service.py

Provides reusable Gmail API helper functions.

---

## `tools/`

Contains individual MCP tools.

Each Python file exposes one or more MCP tools that can be called by any MCP client.

---

# Requirements

- Python 3.11+
- Google Account
- Gmail API enabled
- OAuth Desktop Credentials
- Internet Connection

---

# Installation

Clone the repository.

```bash
git clone https://github.com/namankhandelwal1607/MCP.git
```

Navigate to the Gmail server.

```bash
cd MCP/Gmail-MCP
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

### Linux

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Google Cloud Setup

Before running the server, create OAuth credentials for Gmail.

---

## Step 1 — Create a Google Cloud Project

Open

https://console.cloud.google.com/

Create a new project.

Example:

```
Gmail MCP
```

---

## Step 2 — Enable Gmail API

Navigate to

```
APIs & Services
```

↓

```
Library
```

Search for

```
Gmail API
```

Click

```
Enable
```

---

## Step 3 — Configure OAuth Consent Screen

Go to

```
APIs & Services

↓

OAuth Consent Screen
```

Choose

```
External
```

Fill in

- App Name
- Support Email
- Developer Email

Save.

---

## Step 4 — Create OAuth Credentials

Navigate to

```
Credentials

↓

Create Credentials

↓

OAuth Client ID
```

Application Type

```
Desktop App
```

Download the JSON file.

Rename it to

```
credentials.json
```

Place it inside

```text
Gmail-MCP/
```

---

# OAuth Authentication

The first time you run the server, a browser window opens automatically.

Log in with the Google account you want to use.

After successful authentication, a file named

```text
token.json
```

is automatically generated.

The server will reuse this token for future sessions, so authentication is only required once unless the token expires or is deleted.

---

# Authentication Flow

```text
credentials.json
        │
        ▼
 Browser Login
        │
        ▼
 Google OAuth
        │
        ▼
 token.json
        │
        ▼
 Gmail API Access
```

---

# Required Files

Your project directory should now contain:

```text
Gmail-MCP/

credentials.json

token.json
```

If `token.json` is deleted, the OAuth login process will run again the next time the server starts.

---

---

# Environment Variables

The Gmail MCP Server uses the following environment variables.

```env
GOOGLE_CREDENTIALS=credentials.json
GOOGLE_TOKEN=token.json
```

## GOOGLE_CREDENTIALS

Path to the Google OAuth credentials file downloaded from Google Cloud Console.

Example

```env
GOOGLE_CREDENTIALS=credentials.json
```

---

## GOOGLE_TOKEN

Path to the OAuth access token generated after the first successful login.

Example

```env
GOOGLE_TOKEN=token.json
```

---

# Running the Server

Activate the virtual environment.

### Linux

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Start the server.

```bash
python server.py
```

If everything is configured correctly, the MCP server starts and exposes all Gmail tools.

On the first run, your browser will open automatically for Google authentication.

---

# Available MCP Tools

The server exposes the following tools.

| Tool | Description |
|------|-------------|
| `read_latest_emails` | Read the latest emails |
| `read_unread_emails` | Read unread emails |
| `search_emails` | Search emails using Gmail query syntax |
| `read_email_by_id` | Read a specific email |
| `send_email` | Send a new email |
| `reply_email` | Reply to an existing email thread |
| `save_draft` | Save an email as a draft |

---

# Tool Documentation

## read_latest_emails

Returns the most recent emails from the user's mailbox.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_results` | Integer | Maximum number of emails to return |

### Example

```python
read_latest_emails(max_results=5)
```

Returns

```text
Subject
From
Date
Snippet
```

---

## read_unread_emails

Returns unread emails.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_results` | Integer | Number of unread emails |

Example

```python
read_unread_emails(max_results=10)
```

---

## search_emails

Searches Gmail using the standard Gmail search syntax.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | String | Gmail search query |
| `max_results` | Integer | Maximum emails |

Examples

```python
search_emails(
    query="from:boss@gmail.com"
)
```

```python
search_emails(
    query="label:important"
)
```

```python
search_emails(
    query="has:attachment"
)
```

```python
search_emails(
    query="newer_than:7d"
)
```

```python
search_emails(
    query="is:unread"
)
```

---

## read_email_by_id

Returns the complete contents of a specific email.

### Parameters

| Parameter | Type |
|-----------|------|
| email_id | String |

Example

```python
read_email_by_id(
    email_id="18f4ad7..."
)
```

Returns

- Subject
- Sender
- Receiver
- Date
- Plain Text Body
- HTML Body (if available)

---

## send_email

Sends a new email.

### Parameters

| Parameter | Description |
|-----------|-------------|
| to | Recipient email |
| subject | Email subject |
| body | Email body |

Example

```python
send_email(
    to="john@gmail.com",
    subject="Meeting",
    body="Let's meet tomorrow."
)
```

---

## reply_email

Replies to an existing email thread.

### Parameters

| Parameter | Description |
|-----------|-------------|
| email_id | Original email ID |
| body | Reply body |

Example

```python
reply_email(
    email_id="18f4ad...",
    body="Thanks for the update!"
)
```

The reply is automatically added to the existing Gmail conversation thread.

---

## save_draft

Creates a draft email without sending it.

### Parameters

| Parameter | Description |
|-----------|-------------|
| to | Recipient |
| subject | Draft subject |
| body | Draft body |

Example

```python
save_draft(
    to="alice@gmail.com",
    subject="Project Update",
    body="Draft message..."
)
```

The draft is saved in the Gmail Drafts folder.

---

# Typical Workflow

```text
User Prompt
      │
      ▼
MCP Client
      │
      ▼
Gmail MCP Server
      │
      ▼
Selected Tool
      │
      ▼
Gmail API
      │
      ▼
Response
```

---

# Example Natural Language Requests

Since the server follows the MCP specification, clients like Cursor or LangGraph can automatically invoke the appropriate tool.

Examples:

> Show me my latest emails.

↓

Uses

```
read_latest_emails
```

---

> Do I have any unread emails?

↓

Uses

```
read_unread_emails
```

---

> Search emails from Amazon.

↓

Uses

```
search_emails
```

---

> Send an email to Alice saying I'll be late.

↓

Uses

```
send_email
```

---

> Reply to the latest email saying thank you.

↓

Uses

```
reply_email
```

---

> Save this message as a draft.

↓

Uses

```
save_draft
```

---

# Error Handling

The server handles common Gmail API errors gracefully.

Possible errors include:

- Invalid OAuth credentials
- Expired access token
- Missing permissions
- Invalid email ID
- Network connectivity issues
- Gmail API quota exceeded

Meaningful error messages are returned to the MCP client whenever possible.

---

# Security Notes

- Never commit `credentials.json` to version control.
- Never commit `token.json`.
- Add both files to `.gitignore`.
- Keep your Google Cloud OAuth credentials private.
- Grant only the minimum required Gmail API scopes.

```gitignore
credentials.json
token.json
```

---

# Using with Cursor

Cursor has native support for the **Model Context Protocol (MCP)**, allowing it to automatically discover and invoke tools exposed by this server.

## Step 1 — Open MCP Settings

Open:

```
Settings
    ↓
Features
    ↓
MCP
```

Click **Add New MCP Server**.

---

## Step 2 — Configure the Server

### Linux

```json
{
  "mcpServers": {
    "gmail": {
      "command": "/absolute/path/Gmail-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Gmail-MCP/server.py"
      ]
    }
  }
}
```

---

### Windows (WSL)

```json
{
  "mcpServers": {
    "gmail": {
      "command": "wsl",
      "args": [
        "bash",
        "-lc",
        "cd /home/user/MCP/Gmail-MCP && ./venv/bin/python server.py"
      ]
    }
  }
}
```

Replace the paths with your own project location.

After saving the configuration, Cursor automatically launches the server and discovers all available tools.

---

## Example Prompts

Once connected, you can ask Cursor questions such as:

```
Show me my latest emails.
```

```
Do I have any unread emails?
```

```
Search emails from Google.
```

```
Reply to the latest email thanking them.
```

```
Send an email to john@example.com about tomorrow's meeting.
```

---

# Using with Claude Desktop

Claude Desktop also supports the Model Context Protocol.

Add the server to your Claude MCP configuration.

Example:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "/absolute/path/Gmail-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Gmail-MCP/server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after saving the configuration.

The Gmail tools will automatically become available to Claude.

---

# Using with LangGraph

This repository also includes a LangGraph agent that connects to MCP servers dynamically.

Set the following environment variables inside the Main Agent.

```env
GROQ_API_KEY=your_groq_api_key

MCP_PYTHON=/absolute/path/Gmail-MCP/venv/bin/python

MCP_SERVER=/absolute/path/Gmail-MCP/server.py
```

Then run:

```bash
python main.py
```

The LangGraph agent will:

1. Launch the Gmail MCP server.
2. Discover all available tools.
3. Select the appropriate tool based on the user's request.
4. Execute the tool.
5. Return the response.

No additional integration code is required inside the Gmail server.

---

# Example Workflow

```text
User
 │
 ▼
LangGraph Agent
 │
 ▼
MCP Client
 │
 ▼
Gmail MCP Server
 │
 ▼
Gmail Tool
 │
 ▼
Google Gmail API
 │
 ▼
Response
```

---

# Troubleshooting

## Browser Does Not Open

If the authentication page does not open automatically:

- Verify that `credentials.json` exists.
- Ensure OAuth Desktop credentials were created.
- Delete `token.json` and restart the server.

---

## `FileNotFoundError: credentials.json`

The OAuth credentials file is missing.

Make sure the following file exists:

```text
Gmail-MCP/
└── credentials.json
```

---

## `token.json` Not Found

This is expected on the first run.

The file is generated automatically after successful authentication.

---

## `invalid_grant`

This usually means the OAuth refresh token has expired or become invalid.

Solution:

1. Delete `token.json`
2. Restart the server
3. Authenticate again

---

## Gmail API Disabled

If you receive an API access error:

1. Open Google Cloud Console.
2. Select your project.
3. Navigate to **APIs & Services → Library**.
4. Enable the **Gmail API**.

---

## Permission Denied

Ensure that the authenticated Google account has granted all requested Gmail permissions during the OAuth flow.

If permissions were denied, delete `token.json` and authenticate again.

---

## Server Does Not Start

Verify:

- Python version is 3.11 or newer.
- Virtual environment is activated.
- Dependencies are installed.

```bash
pip install -r requirements.txt
```

---

## Cursor Cannot Find Tools

Check:

- The Python executable path is correct.
- The `server.py` path is correct.
- The server starts successfully from the terminal.
- Cursor has been restarted after updating the MCP configuration.

---

# Frequently Asked Questions

### Can I use multiple Gmail accounts?

Yes.

Each account can have its own `credentials.json` and `token.json`.

---

### Can I deploy this server remotely?

Yes.

Any environment capable of running Python and accessing the Gmail API can host the server.

---

### Does this server store my emails?

No.

The server only retrieves or sends data through the official Gmail API.

No email data is stored locally except the OAuth authentication token.

---

### Can I extend the server?

Yes.

Simply create a new tool inside the `tools/` directory and register it in `server.py`.

Examples:

- Delete emails
- Mark emails as read
- Move emails to labels
- Download attachments
- Manage labels

---