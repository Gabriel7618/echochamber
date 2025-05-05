import requests

# Wikipedia API
def WIKIPEDIA(search):
    return f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search}&format=json"

def DUCKDUCKGO(search):
    return f"https://api.duckduckgo.com/?q={search}&format=json&no_html=1"

def NEWSAPI(search, api_key):
    return f"https://newsapi.org/v2/everything?q={search}&apiKey={api_key}"

# Get articles from all sources
def getarticles(search, newsapi_key=None):
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
                for article in articles[:5]:  # Limit to 5 results
                    links.append((article["title"], article["url"]))
        except Exception as e:
            print("NewsAPI error:", e)

    return links
