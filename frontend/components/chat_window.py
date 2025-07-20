import dash_bootstrap_components as dbc
from dash import html

chat_window = dbc.Card([
    dbc.CardHeader("Chat"),
    dbc.CardBody([
        html.Div(id="chat-history", children=["Chat history will appear here."]),
        dbc.Input(id="chat-input", placeholder="Type your message...", type="text", className="mt-2"),
        dbc.Button("Send", id="send-button", color="primary", className="mt-2")
    ])
], style={"height": "100%"})
