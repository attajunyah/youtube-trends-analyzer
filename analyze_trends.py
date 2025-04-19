import pandas as pd
from pymongo import MongoClient
import certifi

# === Connect to MongoDB and Load Data ===
client = MongoClient(
    "mongodb+srv://mikexzibit25:uojFHj9cqd556EVD@youtube-trends-cluster.yo4njp6.mongodb.net/?retryWrites=true&w=majority&appName=Youtube-Trends-Cluster",
    tlsCAFile=certifi.where()
)
db = client["youtube_trends"]
collection = db["cleaned_videos"]
df = pd.DataFrame(list(collection.find()))

# === 1. Which channel appears the most? ===
most_frequent_channels = df["channel"].value_counts().head(5)
print("\n🎥 Top 5 Most Frequent Channels:")
print(most_frequent_channels)

# === 2. What category gets the most views on average? ===
# (Optional: you could later map category_id to actual names using YouTube category API)
avg_views_per_category = df.groupby("category_id")["views"].mean().sort_values(ascending=False).head(5)
print("\n📊 Top 5 Categories by Average Views:")
print(avg_views_per_category)

# === 3. What are the top 10 most used tags? ===
from collections import Counter

all_tags = df["tags"].explode().dropna()
tag_counts = Counter(all_tags)
top_tags = tag_counts.most_common(10)
print("\n🏷️ Top 10 Most Used Tags:")
for tag, count in top_tags:
    print(f"{tag}: {count} times")

# === 4. What is the average like-to-view ratio? ===
df["like_to_view_ratio"] = df["likes"] / df["views"]
avg_ratio = df["like_to_view_ratio"].mean()
print(f"\n❤️ Average Like-to-View Ratio: {avg_ratio:.4f}")

# === 5. Which video has the most engagement (likes + comments)? ===
df["engagement"] = df["likes"] + df["comments"]
top_engaged = df.sort_values("engagement", ascending=False)[["title", "channel", "likes", "comments", "engagement"]].head(1)
print("\n🔥 Most Engaging Video:")
print(top_engaged.to_string(index=False))

# Let’s take the insights we generated (like top channels, average views per category, etc.)

summary_collection = db["trending_summary"]
summary_collection.drop()  # Clear old summary

# Prepare summary data
summary_doc = {
    "most_frequent_channels": most_frequent_channels.to_dict(),
    "avg_views_per_category": avg_views_per_category.to_dict(),
    "top_tags": {tag: count for tag, count in top_tags},
    "avg_like_to_view_ratio": round(avg_ratio, 4),
    "top_engagement_video": top_engaged.iloc[0].to_dict()
}

# Insert summary document
summary_collection.insert_one(summary_doc)
print("\n[✓] Summary document stored in 'trending_summary'")
