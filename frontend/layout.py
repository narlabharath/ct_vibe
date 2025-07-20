import dash_bootstrap_components as dbc
from dash import html
from components.sidebar import get_sidebar
from components.chat_window import chat_window
from components.file_panel import file_panel

layout = dbc.Container([
    dbc.Row([
        dbc.Col(get_sidebar(), width=3, id="session-sidebar"),
        dbc.Col(chat_window, width=6, id="chat-window"),
        dbc.Col(file_panel, width=3, id="file-panel"),
    ], className="g-0", style={"height": "100vh"})
], fluid=True)
