import sqlite3
import time
import requests
import os
from datetime import datetime, timedelta
from classifier import classify
import random
import concurrent.futures

# ======= CONFIG ========
DATABASE = "search_cache.db"
CACHE_DURATION_MINUTES = 30
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

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
                    classification INTEGER,
                    query_id INTEGER,
                    title TEXT,
                    url TEXT,
                    body TEXT,
                    FOREIGN KEY(query_id) REFERENCES queries(id)
                )''')
    conn.commit()
    conn.close()

# ======= API SOURCES ========
def WIKIPEDIA(search):
    return f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search}&format=json"

def NEWSAPI_EVERYTHING(search):
    return f"https://newsapi.org/v2/everything?q={search}&apiKey={NEWSAPI_KEY}"

def NEWSAPI_TOP(search):
    return f"https://newsapi.org/v2/top-headlines?q={search}&apiKey={NEWSAPI_KEY}"

def HACKER_NEWS(search):
    return f"https://hn.algolia.com/api/v1/search?query={search}"

def DUCKDUCKGO(search):
    return f"https://api.duckduckgo.com/?q={search}&format=json&no_html=1"

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
            c.execute("SELECT title, url, body, classification FROM links WHERE query_id = ?", (query_id,))
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
    for title, url, body, classification in links:
        c.execute("INSERT INTO links (query_id, title, url, body, classification) VALUES (?, ?, ?, ?, ?)",
                  (query_id, title, url, body, classification))
    conn.commit()
    conn.close()

# ======= MAIN FUNCTION ========
def getarticles(search):
    # Check cache
    cached = get_cached_links(search)
    if cached:
        return cached

    links = []

    def fetch_wikipedia():
        try:
            response = requests.get(WIKIPEDIA(search))
            if response.status_code == 200:
                content = response.json().get("query", {}).get("search", [])[:4]
                results = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    classify_futures = {
                        executor.submit(classify, search, page["title"], page.get("snippet", "")): page
                        for page in content
                    }
                    for future in concurrent.futures.as_completed(classify_futures):
                        page = classify_futures[future]
                        try:
                            classification = future.result()
                            results.append((page["title"], f"http://en.wikipedia.org/?curid={page['pageid']}", page.get("snippet", ""), classification))
                        except Exception as e:
                            print("Wikipedia classification error:", e)
                return results
        except Exception as e:
            print("Wikipedia error:", e)
        return []

    def fetch_duckduckgo():
        try:
            response = requests.get(DUCKDUCKGO(search))
            if response.status_code == 200:
                data = response.json()
                if data.get("AbstractText"):
                    title = "DuckDuckGo Abstract"
                    url = data["AbstractURL"]
                    body = data["AbstractText"]
                    classification = classify(search, title, body)
                    return [(title, url, body, classification)]
        except Exception as e:
            print("DuckDuckGo error:", e)
        return []

    def fetch_newsapi_top():
        try:
            response = requests.get(NEWSAPI_TOP(search))
            if response.status_code == 200:
                articles = response.json().get("articles", [])[:30]
                results = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    classify_futures = {
                        executor.submit(classify, search, article["title"], article.get("description", "")): article
                        for article in articles
                    }
                    for future in concurrent.futures.as_completed(classify_futures):
                        article = classify_futures[future]
                        try:
                            classification = future.result()
                            results.append((article["title"], article["url"], article.get("description", ""), classification))
                        except Exception as e:
                            print("NewsAPI TOP classification error:", e)
                return results
        except Exception as e:
            print("NewsAPI TOP error:", e)
        return []

    def fetch_newsapi_everything():
        try:
            response = requests.get(NEWSAPI_EVERYTHING(search))
            if response.status_code == 200:
                articles = response.json().get("articles", [])[:30]
                results = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    classify_futures = {
                        executor.submit(classify, search, article["title"], article.get("description", "")): article
                        for article in articles
                    }
                    for future in concurrent.futures.as_completed(classify_futures):
                        article = classify_futures[future]
                        try:
                            classification = future.result()
                            results.append((article["title"], article["url"], article.get("description", ""), classification))
                        except Exception as e:
                            print("NewsAPI EVERYTHING classification error:", e)
                return results
        except Exception as e:
            print("NewsAPI EVERYTHING error:", e)
        return []

    def fetch_hackernews():
        try:
            response = requests.get(HACKER_NEWS(search))
            if response.status_code == 200:
                posts = response.json().get("hits", [])[:5]
                results = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    classify_futures = {
                        executor.submit(classify, search, post.get("title") or post.get("story_title"), post.get("text", "")): post
                        for post in posts if post.get("title") or post.get("story_title")
                    }
                    for future in concurrent.futures.as_completed(classify_futures):
                        post = classify_futures[future]
                        try:
                            classification = future.result()
                            title = post.get("title") or post.get("story_title")
                            url = post.get("url") or f"https://news.ycombinator.com/item?id={post['objectID']}"
                            results.append((title, url, post.get("text", ""), classification))
                        except Exception as e:
                            print("Hacker News classification error:", e)
                return results
        except Exception as e:
            print("Hacker News error:", e)
        return []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        api_futures = [
            executor.submit(fetch_wikipedia),
            executor.submit(fetch_duckduckgo),
            executor.submit(fetch_newsapi_top),
            executor.submit(fetch_newsapi_everything),
            executor.submit(fetch_hackernews),
        ]
        for future in concurrent.futures.as_completed(api_futures):
            try:
                links.extend(future.result())
            except Exception as e:
                print("API thread error:", e)

    # Cache and return
    cache_links(search, links)
    random.shuffle(links)
    return links

# ======= INIT DB ON IMPORT ========
init_db()
