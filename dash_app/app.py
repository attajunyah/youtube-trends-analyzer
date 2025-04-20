import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_app.utils import get_summary_data
from dash_app.layout import create_dashboard_layout

from dash_app.charts import (
    get_top_channels_chart,
    get_avg_views_by_category_chart,
    get_top_tags_list,
    get_engagement_info,
    get_like_to_view_ratio
)


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

@app.callback(
    Output("your-charts-container", "children"),
    Input("data-mode", "value")
)
def update_dashboard_content(mode):
    summary = get_summary_data(mode)

    return [
        dbc.Row([
            dbc.Col([
                html.H4("Top 5 Most Frequent Channels", className="mt-4"),
                dcc.Graph(figure=get_top_channels_chart(summary))
            ], width=6),
            dbc.Col([
                html.H4("Average Views by Category ID", className="mt-4"),
                dcc.Graph(figure=get_avg_views_by_category_chart(summary))
            ], width=6)
        ]),

        dbc.Row([
            dbc.Col([
                html.H4("Top 10 Tags", className="mt-4"),
                html.Ul([html.Li(f"{tag}: {count}") for tag, count in get_top_tags_list(summary)])
            ], width=4),
            dbc.Col([
                html.H4("Avg Like-to-View Ratio ❤️", className="mt-4"),
                html.H2(f"{get_like_to_view_ratio(summary):.4f}", className="text-center text-success")
            ], width=4),
            dbc.Col([
                html.H4("🔥 Most Engaging Video", className="mt-4"),
                html.P(f"Title: {summary['top_engagement_video']['title']}"),
                html.P(f"Channel: {summary['top_engagement_video']['channel']}"),
                html.P(f"Likes: {summary['top_engagement_video']['likes']:,}"),
                html.P(f"Comments: {summary['top_engagement_video']['comments']:,}")
            ], width=4)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🧠 AI-Powered Weekly Summary"),
                    dbc.CardBody(dcc.Markdown(summary.get("llm_summary", "No summary available.")))
                ], color="light", outline=True, className="mt-4")
            ], width=12)
        ])
    ]

# Initial layout
app.layout = create_dashboard_layout(app)

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
