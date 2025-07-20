
# Backend API Documentation: File-Based Chat System

This backend implements a file-based session and chat management system for a chat application. All data is stored in the filesystem for transparency and easy debugging. The API is built with FastAPI and is organized for extensibility and clarity.

---

## Table of Contents
- [API Overview](#api-overview)
- [Important Files & Structure](#important-files--structure)
- [How to Run](#how-to-run)
- [Design Decisions](#design-decisions)
- [Next Steps](#next-steps)

---

## API Overview

### Root
- **GET /**: Health check or root descriptor endpoint.

### Auth
- **POST /login**: Simulated login for a default hardcoded user ("testuser"). Mirrors authentication flows for future extensibility.

### Session Management
- **GET /sessions**: Lists all sessions for the current user by reading `metadata.json` from each session folder under `sessions/testuser/`.
- **GET /sessions/{session_id}/files**: Lists all uploaded files in a given session directory.
- **GET /sessions/{session_id}/files/{filename}**: Serves a specific uploaded file for download or inspection.
- **POST /upload**: Handles file uploads and creates a new session. Each session folder stores CSV files, metadata, and a chat log.
- **POST /sessions/{session_id}/rename**: Renames the session folder and updates both `session_name` and `session_id` in `metadata.json`.

### Chat Interaction
- **POST /query**: Accepts a question and session_id, stores both question and answer in a chat log (`chat.json`).
- **GET /sessions/{session_id}/chat**: Returns the entire chat log (question-answer pairs) for the session.

---

## Important Files & Structure

**Key Directories & Files:**

- `backend/app/main.py`: FastAPI app entry point. Includes the API router.
- `backend/app/api/routes.py`: All API endpoints and route logic, organized by section (Auth, Session, Chat, Helpers).
- `backend/app/services/session.py`: Helper for saving session metadata.
- `backend/sessions/testuser/`: All session data for the hardcoded user. Each session is a folder containing:
  - `metadata.json`: Session metadata (session_id, session_name, created_at, filenames).
  - `files/`: Uploaded CSV files for the session.
  - `chat.json`: Chat log (list of question-answer pairs).
- `CONTEXT.md`, `backend/README.md`: Project and backend documentation.

**Directory Example:**

```
backend/
  app/
    main.py
    api/routes.py
    services/session.py
  sessions/
    testuser/
      sess_20250720_091650/
        metadata.json
        files/
          valid_expenses.csv
        chat.json
      my-session_20250720_120000/
        ...
```

---

## How to Run

1. **Set up Python environment:**
   - Use Python 3.9+
   - (Recommended) Create and activate a virtual environment:
     ```bash
     python3.9 -m venv .venv
     source .venv/bin/activate
     ```
2. **Install dependencies:**
   - From the project root or backend/app directory:
     ```bash
     pip install fastapi uvicorn pydantic python-multipart
     ```
3. **Run the FastAPI server:**
   - From `backend/app/`:
     ```bash
     uvicorn main:app --reload
     ```
   - The API will be available at `http://localhost:8000/`
4. **Test endpoints:**
   - Use Swagger UI at `http://localhost:8000/docs` for interactive API testing.

---

## Design Decisions

- **File-Based Storage**: No database is used; all data is stored in the filesystem for transparency and easy debugging.
- **Hardcoded User**: All endpoints currently operate for the user "testuser" for development simplicity.
- **Modular Routes**: Endpoints are grouped by function (Session, Chat, Auth) for maintainability.
- **Extensibility**: The structure allows for easy addition of authentication, user scoping, or file pre-processing in the future.

---

## Next Steps

- Begin frontend integration.
- Optional: Add DELETE endpoints for sessions or individual files.
- Optional: Add endpoint to update or delete specific chat log entries.
- Add real authentication and user management.
- Add file validation/type checking on upload.
- Support for dynamic users (not just 'testuser').
- Add filtering, sorting, and pagination for session and file lists.
- Improve error handling and validation throughout the API.

---
