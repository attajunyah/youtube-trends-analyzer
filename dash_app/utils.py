import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

# Load MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI")

def get_summary_data():
    """Connects to MongoDB and retrieves the latest summary analytics."""
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["youtube_trends"]
    summary = db["trending_summary"].find_one()
    return summary
