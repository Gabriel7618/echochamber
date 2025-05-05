import sqlite3
import time
import requests
from datetime import datetime, timedelta

# ======= CONFIG ========
DATABASE = "search_cache.db"
CACHE_DURATION_MINUTES = 30
NEWSAPI_KEY = "NEWS_API_KEY"

# ======= DB SETUP ========
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT UNIQUE,
                    timestamp INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER,
                    title TEXT,
                    url TEXT,
                    FOREIGN KEY(query_id) REFERENCES queries(id)
                )''')
    conn.commit()
    conn.close()

# ======= API SOURCES ========
def WIKIPEDIA(search):
    return f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search}&format=json"

def DUCKDUCKGO(search):
    return f"https://api.duckduckgo.com/?q={search}&format=json&no_html=1"

def NEWSAPI(search, api_key):
    return f"https://newsapi.org/v2/everything?q={search}&apiKey={api_key}"

def HACKER_NEWS(search):
    return f"https://hn.algolia.com/api/v1/search?query={search}"

# ======= DATABASE OPERATIONS ========
def get_cached_links(search):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, timestamp FROM queries WHERE text = ?", (search,))
    row = c.fetchone()
    if row:
        query_id, timestamp = row
        now = int(time.time())
        if now - timestamp < CACHE_DURATION_MINUTES * 60:
            c.execute("SELECT title, url FROM links WHERE query_id = ?", (query_id,))
            links = c.fetchall()
            conn.close()
            return links
        else:
            # Remove expired entries
            c.execute("DELETE FROM links WHERE query_id = ?", (query_id,))
            c.execute("DELETE FROM queries WHERE id = ?", (query_id,))
            conn.commit()
    conn.close()
    return None

def cache_links(search, links):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    now = int(time.time())
    c.execute("INSERT OR REPLACE INTO queries (text, timestamp) VALUES (?, ?)", (search, now))
    query_id = c.execute("SELECT id FROM queries WHERE text = ?", (search,)).fetchone()[0]
    for title, url in links:
        c.execute("INSERT INTO links (query_id, title, url) VALUES (?, ?, ?)", (query_id, title, url))
    conn.commit()
    conn.close()

# ======= MAIN FUNCTION ========
def getarticles(search, newsapi_key=None):
    # Check cache
    cached = get_cached_links(search)
    if cached:
        return cached

    links = []

    # Wikipedia
    try:
        response = requests.get(WIKIPEDIA(search))
        if response.status_code == 200:
            content = response.json().get("query", {}).get("search", [])
            for page in content:
                links.append((page["title"], f"http://en.wikipedia.org/?curid={page['pageid']}"))
    except Exception as e:
        print("Wikipedia error:", e)

    # DuckDuckGo
    try:
        response = requests.get(DUCKDUCKGO(search))
        if response.status_code == 200:
            data = response.json()
            if data.get("AbstractText"):
                links.append(("DuckDuckGo Abstract", data["AbstractURL"]))
    except Exception as e:
        print("DuckDuckGo error:", e)

    # NewsAPI
    if newsapi_key:
        try:
            response = requests.get(NEWSAPI(search, newsapi_key))
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                for article in articles[:5]:
                    links.append((article["title"], article["url"]))
        except Exception as e:
            print("NewsAPI error:", e)

    # Hacker News
    try:
        response = requests.get(HACKER_NEWS(search))
        if response.status_code == 200:
            posts = response.json().get("hits", [])
            for post in posts[:5]:
                title = post.get("title") or post.get("story_title")
                url = post.get("url") or f"https://news.ycombinator.com/item?id={post['objectID']}"
                if title and url:
                    links.append((title, url))
    except Exception as e:
        print("Hacker News error:", e)

    # Cache the results
    cache_links(search, links)

    return links

# ======= INIT DB ON IMPORT ========
init_db()
