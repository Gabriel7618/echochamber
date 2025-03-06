import requests

# SOURCES
def WIKIPEDIA(search):
    return f"http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search}&format=json"

def getarticles(search):
    links = []

    # WIKIPEDIA
    response = requests.get(WIKIPEDIA(search))
    if (response.status_code != 200):
        return {}
    
    content = response.json()["query"]["search"]

    for page in content:
        links.append((page["title"], f"http://en.wikipedia.org/?curid={page["pageid"]}"))

    return links

