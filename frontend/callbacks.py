
from dash import Input, Output, State, ctx, html, dcc
import dash
import requests

def register_callbacks(app: dash.Dash):
    # Login callback
    @app.callback(
        Output("user-store", "data"),
        Output("login-status", "children"),
        Input("login-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True
    )
    def login_user(n_clicks, username, password):
        if not username or not password:
            return dash.no_update, "Please enter username and password."
        try:
            resp = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
            if resp.status_code == 200:
                user = resp.json()
                return user, "Login successful."
            else:
                return None, "Invalid login."
        except Exception:
            return None, "Login failed. Backend not reachable."
    # Update chat window (placeholder)
    @app.callback(
        Output("chat-window", "children"),
        Input("send-button", "n_clicks"),
        State("chat-input", "value"),
        prevent_initial_call=True
    )
    def update_chat(n_clicks, message):
        if message:
            return f"You said: {message}"
        return ""

    # Update session list from backend
    @app.callback(
        Output("session-list", "children"),
        Input("session-refresh-interval", "n_intervals"),
    )
    def update_session_list(n_intervals):
        try:
            resp = requests.get("http://localhost:8000/sessions")
            sessions = resp.json() if resp.status_code == 200 else []
        except Exception:
            sessions = []
        if not sessions:
            return [html.Li("No sessions found.")]
        return [
            html.Li(
                html.Button(
                    s.get("session_name") or s.get("session_id"),
                    id={"type": "session-item", "index": s["session_id"]},
                    n_clicks=0,
                    style={"width": "100%", "textAlign": "left", "background": "none", "border": "none", "padding": "0.5em"}
                )
            ) for s in sessions
        ]

    # Store selected session id when a session is clicked
    @app.callback(
        Output("selected-session-id", "data"),
        Input({"type": "session-item", "index": dash.ALL}, "n_clicks"),
        State({"type": "session-item", "index": dash.ALL}, "id"),
        prevent_initial_call=True
    )
    def select_session(n_clicks_list, ids):
        if not n_clicks_list or not ids:
            return dash.no_update
        for n, id_dict in zip(n_clicks_list, ids):
            if n:
                return id_dict["index"]
        return dash.no_update
