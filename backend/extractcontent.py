'''
If this is your first time running this you need to download all the nltk packages so that rake_nltk can use them

oh and nltk and rake_nltk need to be pip installed

import nltk
nltk.download()
'''

from groq import Groq
from rake_nltk import Rake
import os

def groq_topic(text, instr):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)
    
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": instr
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": text,
            }
        ],
        temperature=0.5,
        top_p=0.5,
        stop=None,
    )

    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def extractContent(prompt):
    # rake thing to get list then crossreference with LLM answer

    # groq key: 
    with open("prompt.txt", "r", encoding="utf-8") as f:
        instr = f.read()

    term = groq_topic(prompt, instr)
    return term
