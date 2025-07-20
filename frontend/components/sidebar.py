import dash_bootstrap_components as dbc
from dash import html, dcc

def get_sidebar():
    return dbc.Card([
        dbc.CardHeader("Sessions"),
        dbc.CardBody([
            # Login form
            html.Div([
                dcc.Input(id="username", type="text", placeholder="Username", className="mb-1", style={"width": "100%"}),
                dcc.Input(id="password", type="password", placeholder="Password", className="mb-1", style={"width": "100%"}),
                html.Button("Login", id="login-btn", n_clicks=0, className="mb-2", style={"width": "100%"}),
                html.Div(id="login-status", className="mb-2"),
                dcc.Store(id="user-store"),
            ], className="mb-3"),
            # Session controls and list
            dbc.Button("New Session", id="new-session-button", color="success", className="mb-2"),
            dcc.Interval(id="session-refresh-interval", interval=10*1000, n_intervals=0),
            dcc.Store(id="selected-session-id"),
            html.Ul(id="session-list", children=["Session list will appear here."])
        ])
    ], style={"height": "100%"})
