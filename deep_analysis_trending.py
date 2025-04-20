import requests
import json
import pandas as pd
from pymongo import MongoClient
from collections import Counter
from dotenv import load_dotenv
import os
import certifi
import time

# === Load env vars ===
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# === MongoDB Setup ===
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["youtube_trends"]
collection = db["deep_trending_videos"]
summary_collection = db["trending_summary_deep"]

# === Fetch up to 200 videos in batches of 50 ===
def fetch_trending_videos(max_results=200, region="US"):
    url = "https://www.googleapis.com/youtube/v3/videos"
    all_items = []

    for _ in range(max_results // 50):
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region,
            "maxResults": 50,
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            items = response.json().get("items", [])
            all_items.extend(items)
            time.sleep(1)  # Respect API quota
        else:
            print("Failed to fetch batch:", response.status_code)
            break

    return all_items

# === Analyze and store ===
def analyze_and_store(data):
    df = pd.json_normalize(data)

    # Basic validation
    df = df[df["statistics.viewCount"].notna()]
    df["views"] = df["statistics.viewCount"].astype(int)
    df["likes"] = pd.to_numeric(df["statistics.likeCount"], errors='coerce').fillna(0).astype(int)
    df["comments"] = pd.to_numeric(df["statistics.commentCount"], errors='coerce').fillna(0).astype(int)

    df["channel"] = df["snippet.channelTitle"]
    df["category_id"] = df["snippet.categoryId"]
    df["tags"] = df["snippet.tags"]

    # Channel frequency
    most_frequent_channels = df["channel"].value_counts().head(10).to_dict()

    # Category views (flattened format)
    agg_df = df.groupby("category_id")["views"].agg(["mean", "median", "max", "min"])
    avg_views_per_category = {
        str(cat): {
            "mean": round(row["mean"], 2),
            "median": round(row["median"], 2),
            "max": int(row["max"]),
            "min": int(row["min"])
        }
        for cat, row in agg_df.iterrows()
    }

    # Tags
    tag_counter = Counter()
    for tags in df["tags"].dropna():
        tag_counter.update(tags)
    top_tags = dict(tag_counter.most_common(20))

    # Engagement
    df["engagement"] = df["likes"] + df["comments"]
    top_engaged = df.sort_values("engagement", ascending=False).iloc[0]

    # Like/view ratio
    df["like_to_view"] = df["likes"] / df["views"]
    avg_ratio = df["like_to_view"].mean()

    # Store raw videos
    collection.drop()
    collection.insert_many(data)

    # Store summary with standardized keys
    summary_collection.drop()
    summary_doc = {
        "most_frequent_channels": most_frequent_channels,
        "avg_views_per_category": avg_views_per_category,
        "top_tags": top_tags,
        "top_engagement_video": {
            "title": top_engaged.get("snippet.title"),
            "channel": top_engaged.get("channel"),
            "likes": int(top_engaged.get("likes")),
            "comments": int(top_engaged.get("comments")),
            "engagement": int(top_engaged.get("engagement"))
        },
        "avg_like_to_view_ratio": round(avg_ratio, 4)
    }

    summary_collection.insert_one(summary_doc)
    print("[✓] Deep summary saved to 'trending_summary_deep'")


# === Main Execution ===
if __name__ == "__main__":
    print("📥 Fetching up to 200 trending videos...")
    videos = fetch_trending_videos()
    print(f"[✓] Fetched {len(videos)} videos")
    analyze_and_store(videos)
    print("📊 Analysis complete.")

    # Optional: Export raw data to JSON
    json_export_path = "deep_trending_videos.json"
    for video in videos:
        video.pop("_id", None)

    with open(json_export_path, "w") as f:
        json.dump(videos, f, indent=2)

    print(f"[✓] Exported raw data to {json_export_path}")
