from dash import Input, Output, callback
import requests
import dash_bootstrap_components as dbc
from dash import html

file_panel = dbc.Card([
    dbc.CardHeader("Files"),
    dbc.CardBody([
        html.Div(id="file-list", children=["File list will appear here."])
    ])
], style={"height": "100%"})


# Callback to update file list when a session is selected
@callback(
    Output("file-list", "children"),
    Input("active-session", "data"),
    prevent_initial_call=True
)
def update_file_list(session_id):
    if not session_id:
        return ["No session selected."]
    try:
        resp = requests.get(f"http://localhost:8000/sessions/{session_id}/files")
        if resp.status_code != 200:
            return ["Failed to fetch files."]
        data = resp.json()
        files = data.get("files") if isinstance(data, dict) else None
        if not files:
            return ["No files found."]
        return [html.Ul([html.Li(f["filename"]) for f in files])]
    except Exception:
        return ["Failed to fetch files."]
