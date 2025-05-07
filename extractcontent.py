'''
If this is your first time running this you need to download all the nltk packages so that rake_nltk can use them

oh and nltk and rake_nltk need to be pip installed

import nltk
nltk.download()
'''

from groq import Groq
def groq_topic(text, key, instr):
    client = Groq(api_key=key)
    
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



import openai
# this function is no longer used because the openai api requires paid credits (which expire too) so i rewrote it using groq like the classifier uses
def gpt_choice(text, key, instr):
    # instr = 'I am writing a web app for classifying news articles, I will give you a user prompt. Give me the most likely phrase that is what the user is searching for news articles about:\nDesired format: <most_likely_phrase>'
    print(key)
    client = openai.OpenAI(api_key=key)
    response = client.responses.create(
        model="gpt-4o",
        instructions=instr,
        input=text,
    )
    #print(response.output_text)
    return response.output_text

from rake_nltk import Rake
def rake(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    phrases = r.get_ranked_phrases()
    #print(phrases)
    return phrases


def main():
    # rake thing to get list then crossreference with LLM answer

    # Groq API key
    key = ""

    # groq key: 
    with open("prompt.txt", "r", encoding="utf-8") as f:
            instr = f.read()
    text = "hi please can you give me some recent news about donald trump, thanks so much!" # this is the user prompt
    phrases = rake(text)
    term = groq_topic(text, key, instr)
    for phrase in phrases:
        if term == phrase: return phrase
        else: return term


if __name__ == "__main__":
    main()
