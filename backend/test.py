from extractcontent import extractContent
from getarticles import getarticles
import os

# content = extractContent("Please give me some articles about Donald Trump")
# articles = getarticles(content)
# # (title, url, body, classification)

# res = [[], [], []]

# for article in articles:
#     res[article[3]].append({"title": article[0], "excerpt": article[2], "url": article[1]})

# for article in res[2]:
#     print(article['url'])

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
print(NEWSAPI_KEY)