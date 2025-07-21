import dash
import dash_bootstrap_components as dbc
from dash import html
from layout import layout
import callbacks
import components.sidebar  # Ensure sidebar callbacks are registered

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "File-Based Chat System"
app.layout = layout

# Register callbacks
callbacks.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
