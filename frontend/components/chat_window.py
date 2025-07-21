import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

chat_window = dbc.Card([
    dbc.CardHeader("Chat"),
    dbc.CardBody([
        dcc.Store(id="chat-history"),
        html.Div([
            html.Div(id="chat-display", children=["Chat history will appear here."], style={
                "overflowY": "auto",
                "flex": 1,
                "marginBottom": "1em",
                "height": "100%",
                "maxHeight": "100%"
            })
        ], style={
            "flex": 1,
            "overflow": "hidden",
            "display": "flex",
            "flexDirection": "column"
        }),
        html.Div([
            dbc.Input(id="chat-input", placeholder="Type your message...", type="text", className="mt-2"),
            dbc.Button("Send", id="send-button", color="primary", className="mt-2")
        ], style={
            "background": "#fff",
            "zIndex": 2,
            "padding": "1em",
            "width": "100%"
        })
    ], style={"height": "calc(100vh - 120px)", "display": "flex", "flexDirection": "column", "padding": 0})
], style={"height": "100%"})
