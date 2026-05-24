import folium
import requests
import webbrowser
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

# 🔑 API Key
API_KEY = "04b51701d45c40bcb5b6b1984ca2a27c"

# 🌍 Locations + Timezones
locations = [
    ("India", "India", 20.5937, 78.9629, "Asia/Kolkata"),
    ("USA", "USA", 37.0902, -95.7129, "America/New_York"),
    ("UK", "United Kingdom", 55.3781, -3.4360, "Europe/London"),
    ("France", "France", 46.2276, 2.2137, "Europe/Paris"),
    ("Japan", "Japan", 36.2048, 138.2529, "Asia/Tokyo"),
    ("Australia", "Australia", -25.2744, 133.7751, "Australia/Sydney"),
    ("New Zealand", "New Zealand", -40.9006, 174.8860, "Pacific/Auckland"),

    # Africa
    ("South Africa", "South Africa", -30.5595, 22.9375, "Africa/Johannesburg"),
    ("Nigeria", "Nigeria", 9.0820, 8.6753, "Africa/Lagos"),

    # Cities
    ("New York", "New York", 40.7128, -74.0060, "America/New_York"),
    ("London", "London", 51.5074, -0.1278, "Europe/London"),
    ("Tokyo", "Tokyo", 35.6762, 139.6503, "Asia/Tokyo"),
    ("Chennai", "Chennai", 13.0827, 80.2707, "Asia/Kolkata"),
    ("Lucknow", "Lucknow", 26.8467, 80.9462, "Asia/Kolkata"),
    ("Delhi", "Delhi", 28.6139, 77.2090, "Asia/Kolkata"),
    ("Mumbai", "Mumbai", 19.0760, 72.8777, "Asia/Kolkata"),
    ("Sydney", "Sydney", -33.8688, 151.2093, "Australia/Sydney"),
    ("Melbourne", "Melbourne", -37.8136, 144.9631, "Australia/Melbourne"),
    ("Auckland", "Auckland", -36.8485, 174.7633, "Pacific/Auckland"),
    ("Paris", "Paris", 48.8566, 2.3522, "Europe/Paris")
]

sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

# 🕒 Local Time
def get_local_time(tz):
    try:
        timezone = pytz.timezone(tz)
        return datetime.now(timezone).strftime("%H:%M:%S")
    except:
        return "N/A"

# 📰 Fetch News (FIXED)
def get_news(query):
    try:
        # 1️⃣ Try top-headlines first
        url1 = f"https://newsapi.org/v2/top-headlines?q={query}&apiKey={API_KEY}"
        response = requests.get(url1, timeout=5)
        data = response.json()

        articles = data.get("articles", [])

        # 2️⃣ Fallback to everything if empty
        if not articles:
            url2 = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
            response = requests.get(url2, timeout=5)
            data = response.json()
            articles = data.get("articles", [])

        articles = articles[:3]

        if not articles:
            return "<b style='color:red;'>No news available for this region</b>"

        html = ""

        for article in articles:
            title = article.get("title", "No Title")
            link = article.get("url", "#")

            sentiment = TextBlob(title).sentiment.polarity

            if sentiment > 0:
                mood = "🟢 Positive"
                sentiment_counts["Positive"] += 1
            elif sentiment < 0:
                mood = "🔴 Negative"
                sentiment_counts["Negative"] += 1
            else:
                mood = "⚪ Neutral"
                sentiment_counts["Neutral"] += 1

            html += f"<a href='{link}' target='_blank'>{title}</a><br><b>{mood}</b><br><br>"

        return html

    except Exception as e:
        return "<b>Error fetching news</b>"

# 🌍 Create Map
def create_map():
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

    for name, query, lat, lon, tz in locations:
        news_html = get_news(query)
        local_time = get_local_time(tz)

        popup_content = f"""
        <div style="background:#1e1e1e; color:white; padding:10px;">
        <h3 style="color:#00ff9f;">{name}</h3>
        <b>🕒 Local Time: {local_time}</b><br><br>
        {news_html}
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=name
        ).add_to(m)

    return m

# 📊 Graph
def plot_graph():
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    # 📊 Bar Chart
    plt.figure()
    plt.bar(labels, values)
    plt.title("Global Sentiment Analysis (Bar Chart)")
    plt.xlabel("Sentiment Type")
    plt.ylabel("Number of News Articles")
    plt.grid(axis='y')
    plt.show()

    # 🥧 Pie Chart
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Sentiment Distribution (Pie Chart)")
    plt.show()

# 🚀 Main
def main():
    print("🌍 Geo News System Running...")

    m = create_map()
    m.save("news_map.html")

    print("✅ Map Ready!")

    webbrowser.open("news_map.html")

    plot_graph()

# ▶️ Run
if __name__ == "__main__":
    main()