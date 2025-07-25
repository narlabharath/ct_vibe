# CT Vibe Frontend

This is the Dash-based frontend for CT Vibe, a session-driven chat and file management system. It provides a modern UI for managing user sessions, uploading and previewing files, and interacting with a FastAPI backend. The frontend is designed for extensibility and a clean user experience.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Key File: components/sidebar.py](#key-file-componentssidebarpy)
- [Other Files](#other-files)
- [How the Pieces Connect](#how-the-pieces-connect)
- [How to Run](#how-to-run)
- [Backend API Endpoints Used](#backend-api-endpoints-used)
- [Extending the Frontend](#extending-the-frontend)
- [About](#about)

---

## Overview

CT Vibe's frontend is a modern, extensible Dash app for session-based chat and file management. It enables users to create, rename, and manage sessions, upload files, and interact with a FastAPI backend—all from a clean, responsive UI.

---

## Features

- **User Authentication**: Login with username and password (UI only; backend integration required).
- **Session Management**:
  - List all sessions for the user.
  - Highlight the active session.
  - Create new sessions by uploading files (with optional session name).
  - Rename existing sessions via a modal dialog.
  - Select and activate sessions.
- **File Upload and Preview**:
  - Upload multiple files when creating a session.
  - Preview uploaded file names before submission.

**Chat Display**:
  - Renders chat responses as an ordered list of output events from the backend `/query` endpoint.
  - Each event is either a text message or a plot image (base64 PNG).
  - Only user/assistant messages and plot images are shown; debug prints/logs are excluded.

- **Responsive UI**:
  - Uses Dash Bootstrap Components for a modern look.
  - Modals for session creation and renaming.
  - Error handling and user feedback for all actions.
- **Live Updates**:
  - Session list auto-refreshes every 10 seconds and after session creation/rename.

---

## File Structure

```text
frontend/
├── app.py              # Dash app entry point; initializes and runs the app
├── callbacks.py        # (Optional) Centralized callback registration (if used)
├── layout.py           # (Optional) App layout definition (if used)
├── components/
│   ├── sidebar.py      # Sidebar UI and all session/file management logic
│   ├── chat_window.py  # (If present) Chat UI component
│   ├── file_panel.py   # (If present) File preview/download component
├── utils/
│   └── api_client.py   # (If present) Helper for backend API requests
└── README.md           # This file
```

---

## Key File: `components/sidebar.py`

- **Purpose**: Implements the sidebar UI and all session/file management features.
- **Main Elements**:
  - Login form
  - Session list (with highlight, select, and rename)
  - New session modal (file upload, preview, optional name)
  - Rename session modal
  - All related Dash callbacks (modal open/close, file upload, session create/rename/select, error handling)
- **Backend Connection**: Uses `requests` to call FastAPI endpoints (e.g., `/sessions`, `/upload`, `/sessions/{id}/rename`).

---

## Other Files

- `app.py`: Entry point; imports and uses the sidebar layout/component.
- `chat_window.py`, `file_panel.py`: (If present) UI for chat and file preview/download.
- `api_client.py`: (If present) Helper functions for backend API calls.

---

## How the Pieces Connect

- `app.py` loads the sidebar (and other components) into the Dash app layout.
- `sidebar.py` manages all session/file UI and logic, and communicates with the backend via HTTP requests.
- All session and file actions (create, rename, select, upload) are handled by Dash callbacks in `sidebar.py`.
- The session list is refreshed automatically and after relevant actions.
- The chat window displays responses as ordered events (text and plot) from the backend, matching the `/query` output format.

---

## How to Run

1. **Install dependencies** (from the `frontend/` directory):
   ```bash
   pip install dash dash-bootstrap-components requests
   ```
2. **Start the FastAPI backend** (from the backend directory):
   ```bash
   uvicorn app.main:app --reload
   ```
3. **Run the Dash frontend** (from the `frontend/` directory):
   ```bash
   python app.py
   ```
4. **Open your browser** to `http://localhost:8050` to use the app.

---

## Backend API Endpoints Used

- `POST /upload` — Create a new session by uploading files
- `GET /sessions` — List all sessions
- `POST /sessions/{session_id}/rename` — Rename a session
- `POST /query` — Send a chat message and receive an ordered list of output events (text/plot) for display

---

## Extending the Frontend

- Add new components to `components/` and import them in `app.py`.
- Add new API helpers to `utils/api_client.py`.
- Add new features or callbacks to `sidebar.py` as needed.

---

## About

CT Vibe is a modern, session-based chat and file management platform. The frontend is built with Dash for rapid development and a clean, interactive user experience. Contributions and suggestions are welcome!
