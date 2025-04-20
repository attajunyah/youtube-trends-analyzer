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
from dash_app.utils import get_llm_summary

def create_dashboard_layout(app):
    summary = get_summary_data()
    top_channels_fig = get_top_channels_chart(summary)
    category_views_fig = get_avg_views_by_category_chart(summary)
    top_tags = get_top_tags_list(summary)
    engagement = get_engagement_info(summary)
    ratio = get_like_to_view_ratio(summary)
    llm_summary = get_llm_summary()

    return dbc.Container([
        dbc.NavbarSimple(
            brand="📊 YouTube Trend Tracker",
            brand_style={"margin": "auto", "text-align": "center", "fontSize": "1.5rem"},
            color="primary",
            dark=True,
            sticky="top"
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
            dbc.Col([
                html.Label("📊 Choose Data Source"),
                dcc.Dropdown(
                    id="data-mode",
                    options=[
                        {"label": "Basic (50 videos)", "value": "basic"},
                        {"label": "Deep (200 videos)", "value": "deep"}
                    ],
                    value="deep",  # default mode
                    clearable=False,
                    style={"width": "300px"}
                )
            ], width=3),
        ], className="my-3"),
        html.Div(id="your-charts-container"),
    ], fluid=True)


