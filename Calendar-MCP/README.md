# Google Calendar MCP Server

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![MCP](https://img.shields.io/badge/MCP-Compatible-success)
![Google Calendar](https://img.shields.io/badge/Google-Calendar-blue)
![OAuth2](https://img.shields.io/badge/Auth-OAuth2-green)

</p>

---

# Overview

The **Google Calendar MCP Server** exposes Google Calendar functionality through the **Model Context Protocol (MCP)**, enabling AI agents and MCP-compatible clients to manage calendar events using natural language.

Instead of interacting directly with the Google Calendar API, clients invoke standardized MCP tools to create, update, search, delete, and retrieve events, as well as check calendar availability.

This server follows the official **Model Context Protocol (MCP)** specification and can be integrated with:

- Cursor
- Claude Desktop
- Continue.dev
- VS Code MCP Extensions
- LangGraph
- FastMCP Clients
- Custom MCP Clients

---

# Features

The Calendar MCP Server currently supports the following operations.

### Event Management

- Create calendar events
- Update existing events
- Delete events
- Retrieve upcoming events
- Search calendar events

### Availability

- Check free/busy status
- Verify availability before scheduling meetings

### AI Integration

The server is designed for seamless integration with AI agents, allowing natural language commands such as:

- "Schedule a meeting tomorrow at 2 PM."
- "What meetings do I have this Friday?"
- "Move my meeting to 4 PM."
- "Am I free next Monday afternoon?"

---

# Project Structure

```text
Calendar-MCP/
│
├── README.md
├── requirements.txt
├── server.py
│
├── gcalendar/
│   ├── auth.py
│   ├── client.py
│   ├── parser.py
│   └── service.py
│
├── tools/
│   ├── availability.py
│   ├── create.py
│   ├── delete.py
│   ├── event.py
│   ├── read.py
│   ├── search.py
│   └── update.py
│
├── credentials.json
├── token.json
│
└── venv/
```

---

# Directory Explanation

## `server.py`

The entry point of the Calendar MCP Server.

It registers all available calendar tools and starts the MCP server.

---

## `gcalendar/`

Contains reusable Google Calendar API helper modules.

### auth.py

Handles Google OAuth authentication.

### client.py

Creates an authenticated Google Calendar client.

### parser.py

Converts Google Calendar API responses into simplified Python objects.

### service.py

Contains reusable helper methods for interacting with the Calendar API.

---

## `tools/`

Each file defines one or more MCP tools that expose Calendar functionality.

| File | Purpose |
|------|---------|
| `create.py` | Create calendar events |
| `update.py` | Update events |
| `delete.py` | Delete events |
| `read.py` | Read upcoming events |
| `search.py` | Search events |
| `availability.py` | Check calendar availability |
| `event.py` | Retrieve event details |

---

# Requirements

Before running the server, ensure you have:

- Python 3.11 or later
- A Google Account
- Google Calendar API enabled
- OAuth Desktop credentials
- Internet connection

---

# Installation

Clone the repository.

```bash
git clone https://github.com/namankhandelwal1607/MCP.git
```

Navigate to the Calendar server.

```bash
cd MCP/Calendar-MCP
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

Before running the Calendar MCP Server, create OAuth credentials for Google Calendar.

---

## Step 1 — Create a Google Cloud Project

Open:

https://console.cloud.google.com/

Create a new project.

Example:

```
Calendar MCP
```

---

## Step 2 — Enable Google Calendar API

Navigate to:

```
APIs & Services
        ↓
Library
```

Search for:

```
Google Calendar API
```

Click:

```
Enable
```

---

## Step 3 — Configure OAuth Consent Screen

Navigate to:

```
APIs & Services
        ↓
OAuth Consent Screen
```

Choose:

```
External
```

Fill in the required information:

- App Name
- User Support Email
- Developer Contact Email

Save the configuration.

---

## Step 4 — Create OAuth Credentials

Navigate to:

```
Credentials
      ↓
Create Credentials
      ↓
OAuth Client ID
```

Application Type:

```
Desktop Application
```

Download the generated JSON file.

Rename it to:

```
credentials.json
```

Place it inside:

```text
Calendar-MCP/
```

---

# OAuth Authentication

The first time the Calendar MCP Server starts, it opens a browser window for Google authentication.

Sign in using the Google account whose calendar you want to manage.

After successful authentication, Google generates:

```text
token.json
```

This token is automatically reused for future sessions, so you only need to authenticate once unless the token is removed or expires.

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
Google Calendar API
```

---

# Required Files

After completing authentication, your project directory should contain:

```text
Calendar-MCP/

credentials.json

token.json
```

If `token.json` is deleted, the server will request authentication again during the next startup.

---

# Calendar API Permissions

The server requests only the permissions required to manage your calendar.

Typical permissions include:

- View calendar events
- Create calendar events
- Update calendar events
- Delete calendar events

Always review the requested permissions before authorizing access.

---

---

# Environment Variables

The Calendar MCP Server uses the following environment variables.

```env
GOOGLE_CREDENTIALS=credentials.json
GOOGLE_TOKEN=token.json
```

## GOOGLE_CREDENTIALS

Path to the OAuth credentials downloaded from Google Cloud Console.

Example

```env
GOOGLE_CREDENTIALS=credentials.json
```

---

## GOOGLE_TOKEN

Path to the OAuth token generated after the first successful login.

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

Start the MCP server.

```bash
python server.py
```

If the configuration is correct, the Calendar MCP Server starts and exposes all available calendar tools.

During the first execution, a browser window opens automatically for Google authentication.

---

# Available MCP Tools

The Calendar MCP Server exposes the following tools.

| Tool | Description |
|------|-------------|
| `create_event` | Create a new calendar event |
| `update_event` | Update an existing calendar event |
| `delete_event` | Delete a calendar event |
| `read_events` | Retrieve upcoming calendar events |
| `search_events` | Search events by keyword or date |
| `check_availability` | Check free/busy availability |
| `get_event_details` | Retrieve complete event information |

---

# Tool Documentation

## create_event

Creates a new Google Calendar event.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | String | Event title |
| `start_time` | String | Event start datetime |
| `end_time` | String | Event end datetime |
| `description` | String | Event description *(optional)* |
| `location` | String | Event location *(optional)* |

### Example

```python
create_event(
    title="Project Meeting",
    start_time="2026-07-20T14:00:00",
    end_time="2026-07-20T15:00:00",
    description="Weekly project discussion",
    location="Conference Room"
)
```

---

## read_events

Retrieves upcoming calendar events.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_results` | Integer | Maximum events to return |

### Example

```python
read_events(max_results=10)
```

Returns

- Event title
- Date
- Time
- Location
- Description

---

## search_events

Searches calendar events using keywords.

### Parameters

| Parameter | Type |
|-----------|------|
| `query` | String |
| `max_results` | Integer |

### Examples

```python
search_events(query="meeting")
```

```python
search_events(query="doctor")
```

```python
search_events(query="vacation")
```

---

## get_event_details

Retrieves complete information about a specific event.

### Parameters

| Parameter | Type |
|-----------|------|
| `event_id` | String |

### Returns

- Title
- Description
- Location
- Start Time
- End Time
- Organizer
- Attendees (if available)

Example

```python
get_event_details(
    event_id="abc123xyz"
)
```

---

## update_event

Updates an existing calendar event.

### Parameters

| Parameter | Description |
|-----------|-------------|
| `event_id` | Event identifier |
| `title` | Updated title *(optional)* |
| `start_time` | Updated start time *(optional)* |
| `end_time` | Updated end time *(optional)* |
| `description` | Updated description *(optional)* |
| `location` | Updated location *(optional)* |

### Example

```python
update_event(
    event_id="abc123",
    start_time="2026-07-20T16:00:00",
    end_time="2026-07-20T17:00:00"
)
```

Only the supplied fields are modified.

---

## delete_event

Deletes an existing calendar event.

### Parameters

| Parameter | Type |
|-----------|------|
| `event_id` | String |

Example

```python
delete_event(
    event_id="abc123"
)
```

The event is permanently removed from the calendar.

---

## check_availability

Checks whether the calendar is free during a specified time interval.

### Parameters

| Parameter | Type |
|-----------|------|
| `start_time` | String |
| `end_time` | String |

Example

```python
check_availability(
    start_time="2026-07-20T14:00:00",
    end_time="2026-07-20T15:00:00"
)
```

Returns

```text
Available
```

or

```text
Busy
```

along with any conflicting events.

---

# Typical Workflow

```text
User Prompt
      │
      ▼
MCP Client
      │
      ▼
Calendar MCP Server
      │
      ▼
Selected Tool
      │
      ▼
Google Calendar API
      │
      ▼
Response
```

---

# Example Natural Language Requests

Because the server follows the MCP specification, clients can automatically invoke the correct tool.

Examples:

> Schedule a meeting tomorrow at 2 PM.

↓

Uses

```
create_event
```

---

> What meetings do I have today?

↓

Uses

```
read_events
```

---

> Search for my doctor appointment.

↓

Uses

```
search_events
```

---

> Move tomorrow's meeting to 4 PM.

↓

Uses

```
update_event
```

---

> Delete my gym session.

↓

Uses

```
delete_event
```

---

> Am I free between 3 PM and 5 PM?

↓

Uses

```
check_availability
```

---

# Error Handling

The Calendar MCP Server handles common Google Calendar API errors gracefully.

Possible errors include:

- Invalid OAuth credentials
- Expired access token
- Missing permissions
- Invalid event ID
- Event not found
- Invalid date/time format
- Network connectivity issues
- Calendar API quota exceeded

Meaningful error messages are returned to the MCP client whenever possible.

---

# Security Notes

- Never commit `credentials.json` to version control.
- Never commit `token.json`.
- Store OAuth credentials securely.
- Grant only the minimum required Calendar API permissions.
- Add the following files to `.gitignore`.

```gitignore
credentials.json
token.json
```

---

# Using with Cursor

Cursor provides built-in support for the **Model Context Protocol (MCP)**, allowing it to automatically discover and invoke the tools exposed by this server.

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
    "calendar": {
      "command": "/absolute/path/Calendar-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Calendar-MCP/server.py"
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
    "calendar": {
      "command": "wsl",
      "args": [
        "bash",
        "-lc",
        "cd /home/user/MCP/Calendar-MCP && ./venv/bin/python server.py"
      ]
    }
  }
}
```

Replace the paths with the location of your project.

After saving the configuration, restart Cursor if required. Cursor will automatically start the Calendar MCP Server and discover all available tools.

---

# Example Prompts

Once connected, you can ask Cursor questions like:

```
What meetings do I have today?
```

```
Schedule a meeting tomorrow at 3 PM.
```

```
Move my project meeting to Friday.
```

```
Delete my dentist appointment.
```

```
Am I free tomorrow afternoon?
```

```
Show my calendar for next week.
```

---

# Using with Claude Desktop

Claude Desktop also supports MCP servers.

Add the following configuration to your Claude Desktop MCP configuration file.

```json
{
  "mcpServers": {
    "calendar": {
      "command": "/absolute/path/Calendar-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Calendar-MCP/server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

The Calendar tools will automatically become available.

---

# Using with LangGraph

This repository includes a LangGraph-based AI agent that dynamically connects to MCP servers.

Configure the following environment variables.

```env
GROQ_API_KEY=your_groq_api_key

MCP_PYTHON=/absolute/path/Calendar-MCP/venv/bin/python

MCP_SERVER=/absolute/path/Calendar-MCP/server.py
```

Run the agent.

```bash
python main.py
```

The LangGraph agent automatically:

1. Starts the Calendar MCP Server.
2. Discovers all available tools.
3. Selects the correct tool based on the user's request.
4. Executes the tool.
5. Returns the response to the user.

No additional integration code is required.

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
Calendar MCP Server
 │
 ▼
Calendar Tool
 │
 ▼
Google Calendar API
 │
 ▼
Response
```

---

# Troubleshooting

## Browser Does Not Open

If the authentication page does not appear automatically:

- Verify that `credentials.json` exists.
- Ensure you created OAuth Desktop credentials.
- Delete `token.json` and restart the server.

---

## `FileNotFoundError: credentials.json`

The OAuth credentials file is missing.

Ensure the following file exists:

```text
Calendar-MCP/
└── credentials.json
```

---

## `token.json` Missing

This is expected on the first execution.

The file is generated automatically after successful authentication.

---

## `invalid_grant`

This indicates that the stored refresh token is no longer valid.

Solution:

1. Delete `token.json`.
2. Restart the server.
3. Authenticate again.

---

## Google Calendar API Not Enabled

If API requests fail, verify that the **Google Calendar API** is enabled in your Google Cloud project.

Navigate to:

```
Google Cloud Console
        ↓
APIs & Services
        ↓
Library
        ↓
Google Calendar API
```

Enable the API if it is disabled.

---

## Invalid Date or Time

Ensure all dates and times use a valid ISO 8601 format.

Example:

```text
2026-07-20T14:00:00
```

---

## Event Not Found

If updating or deleting an event fails:

- Verify that the event ID exists.
- Ensure the authenticated account owns or has access to the calendar containing the event.

---

## Cursor Cannot Discover Tools

Verify:

- The Python executable path is correct.
- The `server.py` path is correct.
- The virtual environment is activated.
- All dependencies are installed.
- Cursor has been restarted after updating the MCP configuration.

---

# Frequently Asked Questions

## Can I use multiple Google Calendars?

Yes.

The authenticated Google account can access all calendars it has permission to manage.

---

## Can I create recurring events?

Yes.

Support for recurring events can be added by extending the event creation logic to include recurrence rules supported by the Google Calendar API.

---

## Does the server store my calendar data?

No.

The server communicates directly with the Google Calendar API.

No calendar events are stored locally except the OAuth authentication token.

---

## Can I extend this server?

Yes.

You can add new tools inside the `tools/` directory and register them in `server.py`.

Examples include:

- Invite attendees
- Create recurring events
- Accept or decline invitations
- Manage reminders
- Manage multiple calendars
- Create all-day events
- List calendars

---