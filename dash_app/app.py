import dash
from dash_app.utils import get_summary_data
from dash_app.layout import create_dashboard_layout

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "YouTube Trend Tracker"

# Load summary data from MongoDB
summary = get_summary_data()

# Set the layout using the loaded data
app.layout = create_dashboard_layout(summary)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
