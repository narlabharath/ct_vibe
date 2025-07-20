import dash
import dash_bootstrap_components as dbc
from dash import html
from layout import layout
import callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "File-Based Chat System"
app.layout = layout

# Register callbacks
callbacks.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
