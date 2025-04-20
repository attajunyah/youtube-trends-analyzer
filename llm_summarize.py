import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from mistralai import Mistral

# === Load .env ===
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)
model = "mistral-large-latest"
MONGO_URI = os.getenv("MONGO_URI")

# === Connect to MongoDB ===
mongo = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = mongo["youtube_trends"]

# === Dynamic Summary Fetcher ===
def get_summary_data(mode="deep"):
    collection_name = "trending_summary_deep" if mode == "deep" else "trending_summary"
    summary = db[collection_name].find_one()
    if summary and "_id" in summary:
        del summary["_id"]
    return summary

# === Format summary as prompt ===
def create_prompt(summary):
    return f"""
Analyze the following YouTube trend data and write a natural language summary for a weekly trend report:

Top Channels:
{json.dumps(summary.get('top_channels', {}), indent=2)}

Average Views per Category (mean, median, max, min):
{json.dumps(summary.get('avg_views_by_category', {}), indent=2)}

Top Tags:
{json.dumps(summary.get('top_tags', {}), indent=2)}

Most Engaging Video:
{json.dumps(summary.get('top_engagement_video', {}), indent=2)}

Average Like-to-View Ratio:
{summary.get('avg_like_to_view_ratio')}

Give a short, friendly, data-driven summary of what's trending on YouTube this week. Use bullet points or paragraph format.
"""

# === Get LLM response ===
def generate_summary(prompt):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return chat_response.choices[0].message.content.strip()

# === Generate and store summary ===
def run_llm_for_mode(mode):
    print(f"\n🤖 Generating LLM-powered summary for {mode} mode...")
    summary = get_summary_data(mode)
    prompt = create_prompt(summary)
    llm_summary = generate_summary(prompt)

    collection_name = "trending_summary_deep" if mode == "deep" else "trending_summary"
    db[collection_name].update_one({}, {"$set": {"llm_summary": llm_summary}})

    print(f"[✓] LLM summary saved to '{collection_name}' → llm_summary")
    print("\n📄 Summary Preview:\n")
    print(llm_summary)

# === Run for both modes ===
if __name__ == "__main__":
    run_llm_for_mode("basic")
    run_llm_for_mode("deep")
