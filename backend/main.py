from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from extractcontent import extractContent
from getarticles import getarticles
from classifier import classify

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


@app.get("/articles/{topic}")
async def get_articles(topic: str):
    return [

            {
                "title": "Test Positive Article",
                "excerpt": f"I'm talking positively about {topic}",
                "url": "https://example.org",
            },

            {
                "title": "Test Positive Article 2",
                "excerpt": f"I'm talking positively about {topic}",
                "url": "https://example.org",
            },

    ]

