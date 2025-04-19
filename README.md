# 📊 YouTube Trends Analyzer

A mini data engineering project that fetches, processes, analyzes, and visualizes trending YouTube videos using Python, MongoDB, and Dash.

---

## 🔧 Features

- ✅ Fetches trending videos from the YouTube Data API
- ✅ Stores raw data in MongoDB Atlas
- ✅ Cleans and normalizes video metadata using pandas
- ✅ Generates insights (top channels, tags, engagement)
- ✅ Stores summaries in a separate MongoDB collection
- ✅ Interactive dashboard with Plotly Dash

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/attajunyah/youtube-trends-analyzer.git
cd youtube-trends-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file with your own keys:

```env
YOUTUBE_API_KEY=your_api_key_here
MONGO_URI=your_mongodb_connection_string
```

### 4. Run the Pipeline

```bash
python fetch_trending.py
python clean_trending.py
python analyze_trends.py
```

### 5. Launch the Dashboard

```bash
python dashboard.py
```

Visit `http://127.0.0.1:8050` in your browser.

---

## 🗂️ Project Structure

```
📦 youtube-trends-analyzer
├── fetch_trending.py        # Fetch trending videos from YouTube API
├── clean_trending.py        # Clean and normalize raw data
├── analyze_trends.py        # Analyze and summarize trends
├── dashboard.py             # Interactive Plotly Dash dashboard
├── .env                     # API and DB credentials (not tracked)
├── .gitignore
└── README.md
```

---

## 🧠 Powered By

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Plotly Dash](https://dash.plotly.com/)
- `pandas`, `python-dotenv`, `certifi`, `pymongo`

---

## 📬 Contact

Built by [Frimpong Atta Junior Osei](https://github.com/attajunyah)

---

## 🛡️ MIT License

Let me know once it's live, and we’ll jump into the **Trend Tracker website build**!
