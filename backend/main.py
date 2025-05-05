from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/articles/{topic}")
async def get_articles(topic: str):
    return {
        "articles": [

            {
                "title": "Test Positive Article",
                "body": f"I'm talking positively about {topic}",
                "link": "https://example.org",
                "date": "03/05/2025",
                "classification": "1",
            },

            {
                "title": "Test Negative Article",
                "body": f"I'm talking negatively about {topic}",
                "link": "https://example.org",
                "date": "03/05/2025",
                "classification": "-1",
            },

            {
                "title": "Test Neutral Article",
                "body": f"I'm talking neutrally about {topic}",
                "link": "https://example.org",
                "date": "03/05/2025",
                "classification": "0",
            },

        ],
    }

