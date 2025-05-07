from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from extractcontent import extractContent
from getarticles import getarticles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or "*" for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/articles/{prompt}")
async def get_articles(prompt: str):
    content = extractContent(prompt)
    articles = getarticles(content)

    # (title, url, body, classification)

    res = {
        "supportive": [],
        "opposing": [],
        "neutral": []
    }

    for article in articles:
        entry = {
            "title": article[0],
            "excerpt": article[2],
            "url": article[1]
        }

        if article[3] == 1:
            res["supportive"].append(entry)
        elif article[3] == -1:
            res["opposing"].append(entry)
        elif article[3] == 0:
            res["neutral"].append(entry)

    return JSONResponse(content=res)
