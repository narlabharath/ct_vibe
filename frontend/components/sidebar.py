from dash import Input, Output, State, html, dcc, callback, ALL
import dash
import requests
import dash_bootstrap_components as dbc
import base64

def get_sidebar():
    return html.Div([
        dbc.Card([
            dbc.CardHeader("Sessions"),
            dbc.CardBody([
                html.Div([
                    dcc.Input(id="username", type="text", placeholder="Username", className="mb-1", style={"width": "100%"}),
                    dcc.Input(id="password", type="password", placeholder="Password", className="mb-1", style={"width": "100%"}),
                    html.Button("Login", id="login-btn", n_clicks=0, className="mb-2", style={"width": "100%"}),
                    html.Div(id="login-status", className="mb-2"),
                    dcc.Store(id="user-store"),
                ], className="mb-3"),
                dbc.Button("New Session", id="new-session-button", color="success", className="mb-2"),
                dcc.Interval(id="session-refresh-interval", interval=10*1000, n_intervals=0),
                html.Div(id="session-list"),
                dcc.Store(id="active-session"),
                dcc.Store(id="rename-session-id"),
                dcc.Store(id="rename-input-store"),
                dcc.Store(id="delete-session-id"),
            ])
        ], style={"height": "100%"}),
        dbc.Modal([
            dbc.ModalHeader("Create New Session"),
            dbc.ModalBody([
                dcc.Upload(
                    id="upload-files", children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    multiple=True,
                    style={"width": "100%", "height": "60px", "lineHeight": "60px", "borderWidth": "1px", "borderStyle": "dashed", "borderRadius": "5px", "textAlign": "center", "marginBottom": "1em"}
                ),
                html.Div(id="uploaded-file-names", style={"marginBottom": "1em"}),
                dcc.Input(id="new-session-name", type="text", placeholder="Session name (optional)", style={"width": "100%", "marginBottom": "1em"}),
                dcc.Store(id="new-session-files"),
                html.Div(id="new-session-error", style={"color": "red", "marginBottom": "1em"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Create Session", id="create-session-btn", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-session-btn", color="secondary")
            ])
        ], id="new-session-modal", is_open=False),
        dbc.Modal([
            dbc.ModalHeader("Rename Session"),
            dbc.ModalBody([
                dcc.Input(id="rename-input", type="text", placeholder="Enter new session name", value="", style={"width": "100%"}),
                html.Div(id="rename-error", style={"color": "red", "marginTop": "0.5em"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Rename", id="rename-confirm-btn", color="primary", className="me-2"),
                dbc.Button("Cancel", id="rename-cancel-btn", color="secondary")
            ])
        ], id="rename-modal", is_open=False),
        dbc.Modal([
            dbc.ModalHeader("Delete Session"),
            dbc.ModalBody([
                html.Div("Are you sure you want to delete this session? This action cannot be undone.", id="delete-modal-body"),
                html.Div(id="delete-error", style={"color": "red", "marginTop": "0.5em"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="delete-confirm-btn", color="danger", className="me-2"),
                dbc.Button("Cancel", id="delete-cancel-btn", color="secondary")
            ])
        ], id="delete-modal", is_open=False)
    ])
# Modal open/close
@callback(
    Output("new-session-modal", "is_open"),
    Output("upload-files", "contents"),
    Output("uploaded-file-names", "children", allow_duplicate=True),
    Output("new-session-name", "value"),
    Output("new-session-error", "children", allow_duplicate=True),
    Input("new-session-button", "n_clicks"),
    Input("cancel-session-btn", "n_clicks"),
    State("new-session-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_new_session_modal(open_click, cancel_click, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger == "new-session-button":
        return True, None, "", "", ""
    if trigger == "cancel-session-btn":
        return False, None, "", "", ""
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Store uploaded files and show preview
@callback(
    Output("new-session-files", "data"),
    Output("uploaded-file-names", "children", allow_duplicate=True),
    Input("upload-files", "contents"),
    State("upload-files", "filename"),
    prevent_initial_call=True
)
def store_uploaded_files(contents, filenames):
    if not contents or not filenames:
        return None, ""
    files = []
    for c, f in zip(contents, filenames):
        files.append({"filename": f, "content": c})
    file_list = html.Ul([html.Li(f["filename"]) for f in files])
    return files, file_list

# Create new session and optionally rename
@callback(
    Output("new-session-error", "children", allow_duplicate=True),
    Output("session-refresh-interval", "n_intervals", allow_duplicate=True),
    Output("active-session", "data", allow_duplicate=True),
    Output("new-session-modal", "is_open", allow_duplicate=True),
    Input("create-session-btn", "n_clicks"),
    State("new-session-files", "data"),
    State("new-session-name", "value"),
    State("session-refresh-interval", "n_intervals"),
    prevent_initial_call=True
)
def create_new_session(n_clicks, files, session_name, n_intervals):
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if not files or len(files) == 0:
        return "Please upload at least one file.", dash.no_update, dash.no_update, dash.no_update
    try:
        upload_files = []
        for f in files:
            content_type, content_string = f["content"].split(",")
            file_bytes = base64.b64decode(content_string)
            upload_files.append(("files", (f["filename"], file_bytes)))
        resp = requests.post("http://localhost:8000/upload", files=upload_files)
        if resp.status_code != 200:
            return "Failed to create session.", dash.no_update, dash.no_update, dash.no_update
        result = resp.json()
        new_session_id = result.get("session_id")
        # Rename if needed
        if session_name and session_name.strip():
            try:
                headers = {"Content-Type": "application/json"}
                rename_resp = requests.post(
                    f"http://localhost:8000/sessions/{new_session_id}/rename",
                    json={"new_name": session_name.strip()},
                    headers=headers
                )
                if rename_resp.status_code != 200:
                    return f"Session created, but rename failed: {rename_resp.text}", (n_intervals or 0) + 1, new_session_id, False
            except Exception as ex:
                return f"Session created, but rename failed: {ex}", (n_intervals or 0) + 1, new_session_id, False
        return "", (n_intervals or 0) + 1, new_session_id, False
    except Exception as e:
        return f"Failed to create session: {e}", dash.no_update, dash.no_update, dash.no_update

@callback(
    Output("session-list", "children"),
    Input("user-store", "data"),
    Input("active-session", "data"),
    Input("session-refresh-interval", "n_intervals"),
    prevent_initial_call=True
)
def render_session_list(user_data, active_session, n_intervals):
    from dash.exceptions import PreventUpdate
    user_key = user_data.get("username") or user_data.get("user_id") if user_data else None
    if not user_data or not user_key:
        raise PreventUpdate
    try:
        resp = requests.get("http://localhost:8000/sessions")
        if resp.status_code != 200:
            return [html.Div("Failed to load sessions.")]
        sessions = resp.json()
    except Exception:
        return [html.Div("Failed to load sessions.")]
    if not sessions:
        return [html.Div("No sessions found.")]
    def get_style(session_id):
        base = {"cursor": "pointer", "padding": "0.5em", "borderBottom": "1px solid #eee", "width": "100%", "textAlign": "left", "background": "none", "border": "none"}
        if active_session and session_id == active_session:
            base["background"] = "#e0e0e0"
        return base
    return [
        html.Div([
            html.Button(
                s.get("session_name") or s.get("session_id"),
                id={"type": "session-item", "index": s["session_id"]},
                n_clicks=0,
                style=get_style(s["session_id"]),
                className="session-entry"
            ),
            html.Button(
                "✏️",
                id={"type": "rename-btn", "index": s["session_id"]},
                n_clicks=0,
                className="rename-btn",
                style={"marginLeft": "0.5em", "border": "none", "background": "transparent", "cursor": "pointer"}
            ),
            html.Button(
                "🗑️",
                id={"type": "delete-btn", "index": s["session_id"]},
                n_clicks=0,
                className="delete-btn",
                style={"marginLeft": "0.5em", "border": "none", "background": "transparent", "cursor": "pointer", "color": "#d9534f"}
            )
        ], className="session-row", style={"display": "flex", "alignItems": "center", "justifyContent": "space-between", "width": "100%"})
        for s in sessions
    ]


# Open Rename Modal When ✏️ Clicked, clear input and set session id
@callback(
    Output("rename-modal", "is_open"),
    Output("rename-session-id", "data"),
    Output("rename-input", "value"),
    Output("rename-error", "children"),
    Input({"type": "rename-btn", "index": ALL}, "n_clicks"),
    State({"type": "rename-btn", "index": ALL}, "id"),
    prevent_initial_call=True
)
def open_rename_modal(n_clicks_list, ids):
    for i, n in enumerate(n_clicks_list):
        if n and ids[i] and "index" in ids[i]:
            return True, ids[i]["index"], "", ""
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Close Rename Modal on Cancel, clear input and session id
@callback(
    Output("rename-modal", "is_open", allow_duplicate=True),
    Output("rename-input", "value", allow_duplicate=True),
    Output("rename-session-id", "data", allow_duplicate=True),
    Output("rename-error", "children", allow_duplicate=True),
    Input("rename-cancel-btn", "n_clicks"),
    prevent_initial_call=True
)
def close_rename_modal(n):
    return False, "", None, ""

# Open Delete Modal When 🗑️ Clicked, set session id
@callback(
    Output("delete-modal", "is_open"),
    Output("delete-session-id", "data"),
    Output("delete-error", "children"),
    Input({"type": "delete-btn", "index": ALL}, "n_clicks"),
    State({"type": "delete-btn", "index": ALL}, "id"),
    prevent_initial_call=True
)
def open_delete_modal(n_clicks_list, ids):
    for i, n in enumerate(n_clicks_list):
        if n and ids[i] and "index" in ids[i]:
            return True, ids[i]["index"], ""
    return dash.no_update, dash.no_update, dash.no_update

# Close Delete Modal on Cancel
@callback(
    Output("delete-modal", "is_open", allow_duplicate=True),
    Output("delete-session-id", "data", allow_duplicate=True),
    Output("delete-error", "children", allow_duplicate=True),
    Input("delete-cancel-btn", "n_clicks"),
    prevent_initial_call=True
)
def close_delete_modal(n):
    return False, None, ""

# Handle Rename Logic via Backend, force refresh, close modal, clear input and session id
@callback(
    Output("rename-error", "children", allow_duplicate=True),
    Output("rename-modal", "is_open", allow_duplicate=True),
    Output("session-refresh-interval", "n_intervals", allow_duplicate=True),
    Output("rename-input", "value", allow_duplicate=True),
    Output("rename-session-id", "data", allow_duplicate=True),
    Input("rename-confirm-btn", "n_clicks"),
    State("rename-session-id", "data"),
    State("rename-input", "value"),
    State("session-refresh-interval", "n_intervals"),
    prevent_initial_call=True
)
def rename_session(n_clicks, session_id, new_name, interval_count):
    if not session_id or not new_name:
        return "Please enter a new name.", dash.no_update, dash.no_update, dash.no_update, dash.no_update
    try:
        resp = requests.post(
            f"http://localhost:8000/sessions/{session_id}/rename",
            json={"new_name": new_name},
            headers={"Content-Type": "application/json"}
        )
        if resp.status_code == 200:
            return "", False, (interval_count or 0) + 1, "", None
        else:
            return f"Rename failed: {resp.text}", dash.no_update, dash.no_update, dash.no_update, dash.no_update
    except Exception as e:
        return f"Rename failed: {e}", dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callback to store active session id when a session is clicked
from dash import ALL, State
@callback(
    Output("active-session", "data", allow_duplicate=True),
    Input({"type": "session-item", "index": ALL}, "n_clicks"),
    State({"type": "session-item", "index": ALL}, "id"),
    prevent_initial_call=True
)
def set_active_session(n_clicks_list, ids):
    if not n_clicks_list or not ids:
        return dash.no_update
    for i, n in enumerate(n_clicks_list):
        if n and ids[i] and "index" in ids[i]:
            print("Clicked session ID:", ids[i]["index"])
            return ids[i]["index"]
    return dash.no_update
