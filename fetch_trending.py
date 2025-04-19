import requests
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")


# === CONFIG ===
REGION = "US"
MAX_RESULTS = 50

# === FETCH DATA FROM YOUTUBE API ===
url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "regionCode": REGION,
    "maxResults": MAX_RESULTS,
    "key": API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()["items"]
    
    # Save raw data to JSON file
    with open("trending_videos.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"[✓] Fetched {len(data)} trending videos for {REGION}")

    # === INSERT INTO MONGODB ===
    client = MongoClient(MONGO_URI)
    db = client["youtube_trends"]
    collection = db["trending_videos"]

    # Optional: drop previous entries to avoid duplicates
    collection.drop()
    
    collection.insert_many(data)
    print(f"[✓] Inserted into MongoDB: {collection.count_documents({})} documents")

else:
    print("[✗] Failed to fetch data:", response.status_code, response.text)
