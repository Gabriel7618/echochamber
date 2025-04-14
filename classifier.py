import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def classify(topic, title, body):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                        "Say Hello World!"
                    ),
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)

    return 0

if __name__ == "__main__":
    classify(None, None, None)

