import dash_bootstrap_components as dbc
from dash import html

file_panel = dbc.Card([
    dbc.CardHeader("Files"),
    dbc.CardBody([
        html.Div(id="file-list", children=["File list will appear here."])
    ])
], style={"height": "100%"})
