# Frontend (Dash App) for File-Based Chat System

This folder contains the Dash-based frontend for the File-Based Chat System. The app provides a modern, multi-panel UI for interacting with the FastAPI backend, managing sessions, uploading files, and chatting with the system.

---

## Features
- **Login Form**: Simulated login (username/password) with backend authentication.
- **Session List**: Dynamic list of sessions fetched from the backend, with clickable selection.
- **File Panel**: Displays files uploaded for the selected session.
- **Chat Window**: Shows chat history and allows sending new questions to the backend.
- **New Session**: Button to trigger file upload and start a new session (to be implemented).
- **Live Updates**: Uses Dash callbacks and polling to keep session and chat data up to date.

---

## File Structure

- `app.py` — Dash entry point, sets up layout and callback registration.
- `layout.py` — Defines the 3-panel layout using Dash Bootstrap Components.
- `callbacks.py` — Contains all Dash callback logic (login, session selection, chat, etc).
- `components/`
  - `sidebar.py` — Sidebar with login form, session list, and new session button.
  - `chat_window.py` — Chat history and input box.
  - `file_panel.py` — File list for the selected session.
- `utils/api_client.py` — Helper functions for calling backend API endpoints.

---

## How to Run

1. **Activate the Python virtual environment** (from project root):
   ```bash
   source .venv/bin/activate
   ```
2. **Install frontend dependencies** (if not already):
   ```bash
   pip install dash dash-bootstrap-components requests
   ```
3. **Start the Dash app** (from the `frontend/` folder):
   ```bash
   python app.py
   ```
4. **Open your browser** to [http://localhost:8050](http://localhost:8050) to use the app.

---

## Development Notes
- The frontend expects the FastAPI backend to be running at `http://localhost:8000`.
- All session and chat actions are currently scoped to a hardcoded user ("testuser") until real authentication is implemented.
- The UI is built with [Dash](https://dash.plotly.com/) and [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/).
- Extend the app by adding more callbacks, file upload logic, and richer chat features as needed.

---

## Next Steps
- Implement file upload and new session creation.
- Connect chat and file panels to backend data.
- Add user feedback and error handling for all actions.
- Polish UI and add more interactivity as needed.
