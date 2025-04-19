# 📊 YouTube Trend Tracker Dashboard

An interactive web dashboard built with [Plotly Dash](https://dash.plotly.com/) that visualizes summarized insights from trending YouTube videos.

---

## 📂 Folder: `dash_app/`

The `dash_app/` directory contains the entire Dash application used to serve and visualize data from MongoDB.

### 📁 Structure

```
dash_app/
├── app.py           # Main Dash server entry
├── utils.py         # Connects to MongoDB and fetches summary data
├── charts.py        # Builds charts from summary data
└── layout.py        # Defines the dashboard layout
```

---

## 🧠 How It Works

```text
YouTube API → Raw DB → Cleaned DB → Summary DB
                              ↓
               DASH APP (reads from summary)
```

| Module       | Purpose                                      |
|--------------|----------------------------------------------|
| `utils.py`   | Connects to MongoDB and loads summary data   |
| `charts.py`  | Generates Plotly figures from the data       |
| `layout.py`  | Arranges the UI layout using Dash components |
| `app.py`     | Boots the app server using Dash              |

---

## 🚀 How to Launch the Dashboard

1. Make sure you've run the full pipeline:
   ```bash
   python fetch_trending.py
   python clean_trending.py
   python analyze_trends.py
   ```

2. Start the dashboard from your project root:
   ```bash
   python -m dash_app.app
   ```

3. Visit it in your browser:
   ```
   http://127.0.0.1:8050/
   ```

---

## 📈 Dashboard Sections

- **Top Channels** — Bar chart of most frequent creators
- **Category Insights** — Avg. views per category ID
- **Top Tags** — Top 10 most used tags across videos
- **Most Engaging Video** — Likes + comments leaderboard
- **Like-to-View Ratio** — Global engagement metric

---

## 🔐 Secret Configuration

Your `.env` file should include the following:

```env
YOUTUBE_API_KEY=your_youtube_api_key
MONGO_URI=your_mongodb_uri
```

Make sure `.env` is listed in `.gitignore` and never committed to GitHub.

---

## 📸 Screenshots (Optional)

You can add screenshots of the dashboard here in the future to showcase your UI.

---

## 🧠 Built By

Frimpong Atta Junior Osei  
> Making data beautiful and insightful 🔍📊
```

---

