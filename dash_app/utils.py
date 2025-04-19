import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

# Load MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["youtube_trends"]

def get_summary_data():
    """Connects to MongoDB and retrieves the latest summary analytics."""
    summary = db["trending_summary"].find_one()
    return summary


# Add get_llm_summary function to fetch the llm_summary
def get_llm_summary():
    summary = db["trending_summary_deep"].find_one()
    return summary.get("llm_summary", "No summary available.")
