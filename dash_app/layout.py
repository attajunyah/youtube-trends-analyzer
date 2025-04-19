from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.charts import (
    get_top_channels_chart,
    get_avg_views_by_category_chart,
    get_top_tags_list,
    get_engagement_info,
    get_like_to_view_ratio
)
from dash_app.utils import get_summary_data

def create_dashboard_layout(app):
    summary = get_summary_data()
    top_channels_fig = get_top_channels_chart(summary)
    category_views_fig = get_avg_views_by_category_chart(summary)
    top_tags = get_top_tags_list(summary)
    engagement = get_engagement_info(summary)
    ratio = get_like_to_view_ratio(summary)

    return dbc.Container([
        # Theme toggle
        dcc.Store(id="theme-store"),
        dbc.NavbarSimple(
            brand="📊 YouTube Trend Tracker",
            color="primary",
            dark=True,
            sticky="top",
            children=[
                dbc.Switch(
                    id="theme-toggle",
                    label="Dark Mode",
                    value=False,
                    style={"color": "white", "marginLeft": "20px"}
                )
            ]
        ),

        dbc.Row([
            dbc.Col([
                html.Label("🌍 Region"),
                dcc.Dropdown(
                    options=[
                        {"label": "United States", "value": "US"},
                        {"label": "United Kingdom", "value": "GB"},
                        {"label": "India", "value": "IN"},
                    ],
                    value="US",
                    placeholder="Select region",
                )
            ], width=3),
            dbc.Col([
                html.Label("🎥 Category"),
                dcc.Dropdown(
                    options=[
                        {"label": "Music", "value": "10"},
                        {"label": "Gaming", "value": "20"},
                        {"label": "News", "value": "25"},
                    ],
                    value="10",
                    placeholder="Select category"
                )
            ], width=3),
        ], className="mt-4"),

        dbc.Row([
            dbc.Col([
                html.H4("Top 5 Most Frequent Channels", className="mt-4"),
                dcc.Graph(figure=top_channels_fig)
            ], width=6),
            dbc.Col([
                html.H4("Average Views by Category ID", className="mt-4"),
                dcc.Graph(figure=category_views_fig)
            ], width=6)
        ]),

        dbc.Row([
            dbc.Col([
                html.H4("Top 10 Tags", className="mt-4"),
                html.Ul([html.Li(f"{tag}: {count}") for tag, count in top_tags])
            ], width=4),
            dbc.Col([
                html.H4("Avg Like-to-View Ratio ❤️", className="mt-4"),
                html.H2(f"{ratio:.4f}", className="text-center text-success")
            ], width=4),
            dbc.Col([
                html.H4("🔥 Most Engaging Video", className="mt-4"),
                html.P(f"Title: {engagement.get('title', 'N/A')}"),
                html.P(f"Channel: {engagement.get('channel', 'N/A')}"),
                html.P(f"Likes: {engagement.get('likes', 0):,}"),
                html.P(f"Comments: {engagement.get('comments', 0):,}")
            ], width=4)
        ])
    ], fluid=True)







# from dash import html, dcc
# from dash_app.charts import (
#     get_top_channels_chart,
#     get_avg_views_by_category_chart,
#     get_top_tags_list,
#     get_engagement_info,
#     get_like_to_view_ratio
# )

# def create_dashboard_layout(summary):
#     # Get charts and data
#     top_channels_fig = get_top_channels_chart(summary)
#     category_views_fig = get_avg_views_by_category_chart(summary)
#     top_tags = get_top_tags_list(summary)
#     engagement = get_engagement_info(summary)
#     ratio = get_like_to_view_ratio(summary)

#     # Build layout
#     return html.Div([
#         html.H1("📊 YouTube Trend Tracker", style={"textAlign": "center", "marginTop": "20px"}),

#         html.Div([
#             html.Div([
#                 html.H3("Top 5 Most Frequent Channels"),
#                 dcc.Graph(figure=top_channels_fig)
#             ], className="six columns"),

#             html.Div([
#                 html.H3("Average Views by Category ID"),
#                 dcc.Graph(figure=category_views_fig)
#             ], className="six columns"),
#         ], className="row", style={"display": "flex"}),

#         html.Div([
#             html.Div([
#                 html.H3("Top 10 Tags"),
#                 html.Ul([html.Li(f"{tag}: {count}") for tag, count in top_tags])
#             ], className="four columns"),

#             html.Div([
#                 html.H3("Avg Like-to-View Ratio"),
#                 html.P(f"{ratio:.4f}", style={"fontSize": "30px", "fontWeight": "bold"})
#             ], className="four columns"),

#             html.Div([
#                 html.H3("🔥 Most Engaging Video"),
#                 html.P(f"Title: {engagement.get('title', 'N/A')}"),
#                 html.P(f"Channel: {engagement.get('channel', 'N/A')}"),
#                 html.P(f"Likes: {engagement.get('likes', 0):,}"),
#                 html.P(f"Comments: {engagement.get('comments', 0):,}")
#             ], className="four columns"),
#         ], className="row", style={"display": "flex", "marginTop": "30px"})
#     ], style={"padding": "40px"})
