# AI Productivity Assistant using Model Context Protocol (MCP)

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-Compatible-success)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-red)
![Google](https://img.shields.io/badge/Google-Gmail%20%26%20Calendar-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# Overview

This repository contains an **AI Productivity Assistant** built using the **Model Context Protocol (MCP)**.

The project consists of independent MCP servers for **Gmail** and **Google Calendar**, along with a **LangGraph-based AI agent** that dynamically discovers and invokes tools exposed by these servers.

Because every server follows the official **Model Context Protocol (MCP)** specification, they can be used independently with any MCP-compatible client or together through the included LangGraph agent.

---

# Project Components

## 📧 Gmail MCP Server

Provides Gmail functionality through MCP.

Features include:

* Read latest emails
* Read unread emails
* Search emails
* Read email by ID
* Send emails
* Reply to emails
* Save drafts

📖 Documentation:

```text
Gmail-MCP/README.md
```

---

## 📅 Google Calendar MCP Server

Provides Google Calendar functionality through MCP.

Features include:

* Create events
* Update events
* Delete events
* Search events
* Read upcoming events
* Check calendar availability

📖 Documentation:

```text
Calendar-MCP/README.md
```

---

## 🤖 LangGraph Main Agent

A LangGraph-based conversational AI agent that connects to one or more MCP servers, discovers their available tools, and executes them automatically using a Groq language model.

📖 Documentation:

```text
Main-Agent/README.md
```

---

# Architecture

```text
                         User
                           │
                           ▼
                  LangGraph Agent
                           │
              MultiServerMCPClient
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
    Gmail MCP Server              Calendar MCP Server
          │                                 │
          ▼                                 ▼
      Gmail API                     Google Calendar API
```

---

# Repository Structure

```text
MCP/
│
├── README.md
│
├── Gmail-MCP/
│   ├── README.md
│   ├── server.py
│   ├── gmail/
│   ├── tools/
│   └── ...
│
├── Calendar-MCP/
│   ├── README.md
│   ├── server.py
│   ├── gcalendar/
│   ├── tools/
│   └── ...
│
└── Main-Agent/
    ├── README.md
    ├── graph.py
    ├── nodes.py
    ├── state.py
    ├── config.py
    └── main.py
```

---

# Technologies Used

### AI & Agent Frameworks

* LangGraph
* LangChain
* Groq
* Llama 3
* Model Context Protocol (MCP)

### Backend

* Python
* FastMCP
* AsyncIO

### Google Services

* Gmail API
* Google Calendar API

---

# Getting Started

Clone the repository.

```bash
git clone https://github.com/namankhandelwal1607/MCP.git

cd MCP
```

Each project is self-contained and includes its own dependencies and documentation.

Refer to the corresponding README for detailed setup instructions.

| Component            | Documentation            |
| -------------------- | ------------------------ |
| Gmail MCP Server     | `Gmail-MCP/README.md`    |
| Calendar MCP Server  | `Calendar-MCP/README.md` |
| LangGraph Main Agent | `Main-Agent/README.md`   |

---

# Running the Projects

Each component can be used independently.

## Gmail MCP Server

```bash
cd Gmail-MCP
python server.py
```

For OAuth setup, environment variables, available tools, and usage examples, refer to:

```text
Gmail-MCP/README.md
```

---

## Calendar MCP Server

```bash
cd Calendar-MCP
python server.py
```

For Google Calendar configuration, authentication, tool documentation, and examples, refer to:

```text
Calendar-MCP/README.md
```

---

## LangGraph Main Agent

```bash
cd Main-Agent
python main.py
```

For MCP server configuration, environment variables, and integration details, refer to:

```text
Main-Agent/README.md
```

---

# Using with Cursor

Both MCP servers can be connected directly to Cursor using its built-in MCP support.

Example configuration:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "/absolute/path/Gmail-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Gmail-MCP/server.py"
      ]
    },
    "calendar": {
      "command": "/absolute/path/Calendar-MCP/venv/bin/python",
      "args": [
        "/absolute/path/Calendar-MCP/server.py"
      ]
    }
  }
}
```

For complete Cursor setup instructions, see:

* `Gmail-MCP/README.md`
* `Calendar-MCP/README.md`

---

# Supported MCP Clients

These MCP servers can be used with any client implementing the Model Context Protocol, including:

* Cursor
* Claude Desktop
* Continue.dev
* VS Code MCP Extensions
* LangGraph
* Custom Python MCP Clients
* FastMCP Applications

---