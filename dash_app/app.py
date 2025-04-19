import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_app.utils import get_summary_data
from dash_app.layout import create_dashboard_layout

# Theme mapping
THEMES = {
    "light": dbc.themes.LUX,
    "dark": dbc.themes.DARKLY
}

# Create the app with a default theme
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[THEMES["light"]],
)
app.title = "YouTube Trend Tracker"
server = app.server

# Initial layout
app.layout = create_dashboard_layout(app)

# Callback to handle theme switching (if layout were dynamically updated)
@app.callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "value")
)
def update_theme(toggle_val):
    return THEMES["dark"] if toggle_val else THEMES["light"]

if __name__ == "__main__":
    app.run(debug=True)




# import dash
# from dash_app.utils import get_summary_data
# from dash_app.layout import create_dashboard_layout


# # Initialize Dash app
# app = dash.Dash(__name__)
# app.title = "YouTube Trend Tracker"

# # Load summary data from MongoDB
# summary = get_summary_data()

# # Set the layout using the loaded data
# app.layout = create_dashboard_layout(summary)

# # Run server
# if __name__ == "__main__":
#     app.run(debug=True)
