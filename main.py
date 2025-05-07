from extractcontent import extractContent
from getarticles import get_articles

content = extractContent("Please give me some articles about Donald Trump")
articles = get_articles(content)

res = [[], [], []]

for article in articles:
    res[article['classification']].append({"title": article['title'], "excerpt": article['body'], "url": article['url']})

print(res[0], res[1], res[2])