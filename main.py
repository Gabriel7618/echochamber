from extractcontent import extractContent
from getarticles import getarticles
from classifier import classify

search = input("Please enter your search query.\n")

# First, process the search string
content = extractContent(search)

# Now, get the article links from content
results = getarticles(content)

# Classify each result

for result in results:
    print(result[0] + " at " + result[1])
