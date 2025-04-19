from pymongo import MongoClient
import certifi
import pandas as pd

# === Connect to MongoDB ===
client = MongoClient(
    "mongodb+srv://mikexzibit25:uojFHj9cqd556EVD@youtube-trends-cluster.yo4njp6.mongodb.net/?retryWrites=true&w=majority&appName=Youtube-Trends-Cluster",
    tlsCAFile=certifi.where()
)
db = client["youtube_trends"]
raw_collection = db["trending_videos"]
clean_collection = db["cleaned_videos"]

# === Load Raw Data ===
raw_data = list(raw_collection.find())
# print(raw_data)

# === Extract & Flatten Relevant Fields ===
cleaned_data = []
for item in raw_data:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})

    cleaned_data.append({
        "video_id": item.get("id"),
        "title": snippet.get("title"),
        "channel": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "category_id": snippet.get("categoryId"),
        "tags": snippet.get("tags", []),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0))
    })

# === Convert to DataFrame ===
df = pd.DataFrame(cleaned_data)

# === Save to New MongoDB Collection ===
clean_collection.drop()
clean_collection.insert_many(df.to_dict("records"))

print(f"[✓] Cleaned and inserted {len(df)} records into 'cleaned_videos'")
