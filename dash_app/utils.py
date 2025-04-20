import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

# Load MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["youtube_trends"]

def get_summary_data(mode="basic"):
    collection_name = "trending_summary" if mode == "basic" else "trending_summary_deep"
    summary = db[collection_name].find_one()
    if summary and "_id" in summary:
        del summary["_id"]
    return summary


# Add get_llm_summary function to fetch the llm_summary
def get_llm_summary():
    summary = db["trending_summary_deep"].find_one()
    return summary.get("llm_summary", "No summary available.")
