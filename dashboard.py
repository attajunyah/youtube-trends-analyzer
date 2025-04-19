import dash
from dash import html, dcc
import plotly.express as px
from pymongo import MongoClient
import pandas as pd
import certifi

# === Load Summary from MongoDB ===
client = MongoClient(
    "mongodb+srv://mikexzibit25:uojFHj9cqd556EVD@youtube-trends-cluster.yo4njp6.mongodb.net/?retryWrites=true&w=majority&appName=Youtube-Trends-Cluster",
    tlsCAFile=certifi.where()
)
db = client["youtube_trends"]
summary = db["trending_summary"].find_one()

# === Convert to DataFrames ===
channels_df = pd.DataFrame(summary["most_frequent_channels"].items(), columns=["Channel", "Count"])
views_df = pd.DataFrame(summary["avg_views_per_category"].items(), columns=["Category ID", "Avg Views"])
tags_list = list(summary["top_tags"].items())
tags_display = html.Ul([html.Li(f"{tag}: {count}") for tag, count in tags_list])
engagement = summary["top_engagement_video"]

# === Build Dash App ===
app = dash.Dash(__name__)
app.title = "YouTube Trending Dashboard"

app.layout = html.Div([
    html.H1("📊 YouTube Trending Summary", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Top 5 Channels"),
            dcc.Graph(figure=px.bar(channels_df, x="Channel", y="Count", color="Channel")),
        ], className="six columns"),

        html.Div([
            html.H3("Average Views by Category ID"),
            dcc.Graph(figure=px.bar(views_df, x="Category ID", y="Avg Views")),
        ], className="six columns"),
    ], className="row"),

    html.Div([
        html.Div([
            html.H3("Top 10 Tags"),
            tags_display
        ], className="six columns"),

        html.Div([
            html.H3("Avg Like-to-View Ratio"),
            html.P(f"{summary['avg_like_to_view_ratio']:.4f}", style={"fontSize": "32px"})
        ], className="three columns"),

        html.Div([
            html.H3("🔥 Top Engaging Video"),
            html.P(f"Title: {engagement['title']}"),
            html.P(f"Channel: {engagement['channel']}"),
            html.P(f"Likes: {engagement['likes']:,} | Comments: {engagement['comments']:,}")
        ], className="three columns"),
    ], className="row"),
], style={"margin": "40px"})

if __name__ == "__main__":
    app.run(debug=True)
