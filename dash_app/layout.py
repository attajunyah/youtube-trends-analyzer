from dash import html, dcc
from dash_app.charts import (
    get_top_channels_chart,
    get_avg_views_by_category_chart,
    get_top_tags_list,
    get_engagement_info,
    get_like_to_view_ratio
)

def create_dashboard_layout(summary):
    # Get charts and data
    top_channels_fig = get_top_channels_chart(summary)
    category_views_fig = get_avg_views_by_category_chart(summary)
    top_tags = get_top_tags_list(summary)
    engagement = get_engagement_info(summary)
    ratio = get_like_to_view_ratio(summary)

    # Build layout
    return html.Div([
        html.H1("📊 YouTube Trend Tracker", style={"textAlign": "center", "marginTop": "20px"}),

        html.Div([
            html.Div([
                html.H3("Top 5 Most Frequent Channels"),
                dcc.Graph(figure=top_channels_fig)
            ], className="six columns"),

            html.Div([
                html.H3("Average Views by Category ID"),
                dcc.Graph(figure=category_views_fig)
            ], className="six columns"),
        ], className="row", style={"display": "flex"}),

        html.Div([
            html.Div([
                html.H3("Top 10 Tags"),
                html.Ul([html.Li(f"{tag}: {count}") for tag, count in top_tags])
            ], className="four columns"),

            html.Div([
                html.H3("Avg Like-to-View Ratio"),
                html.P(f"{ratio:.4f}", style={"fontSize": "30px", "fontWeight": "bold"})
            ], className="four columns"),

            html.Div([
                html.H3("🔥 Most Engaging Video"),
                html.P(f"Title: {engagement.get('title', 'N/A')}"),
                html.P(f"Channel: {engagement.get('channel', 'N/A')}"),
                html.P(f"Likes: {engagement.get('likes', 0):,}"),
                html.P(f"Comments: {engagement.get('comments', 0):,}")
            ], className="four columns"),
        ], className="row", style={"display": "flex", "marginTop": "30px"})
    ], style={"padding": "40px"})
