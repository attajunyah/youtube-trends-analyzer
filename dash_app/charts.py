import plotly.express as px
import pandas as pd

def get_top_channels_chart(summary):
    data = summary.get("most_frequent_channels", {})
    df = pd.DataFrame(data.items(), columns=["Channel", "Count"])
    fig = px.bar(df, x="Channel", y="Count", title="Top 5 Most Frequent Channels", color="Channel")
    return fig

def get_avg_views_by_category_chart(summary):
    data = summary.get("avg_views_per_category", {})
    records = []

    for cat_id, value in data.items():
        # Handle both formats: nested dict OR single float
        if isinstance(value, dict):
            for stat_name, stat_val in value.items():
                records.append({
                    "Category ID": cat_id,
                    "Metric": stat_name.capitalize(),
                    "Value": stat_val
                })
        else:
            records.append({
                "Category ID": cat_id,
                "Metric": "Average",
                "Value": value
            })

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x="Category ID",
        y="Value",
        color="Metric",
        barmode="group",
        title="Category-wise Views (Mean, Median, Max, Min)"
    )
    return fig



def get_top_tags_list(summary):
    tags = summary.get("top_tags", {})
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    return sorted_tags[:10]

def get_engagement_info(summary):
    return summary.get("top_engagement_video", {})

def get_like_to_view_ratio(summary):
    return summary.get("avg_like_to_view_ratio", 0)
