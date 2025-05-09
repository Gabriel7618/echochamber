# echochamber

## API Keys

The classifier uses [Groq](https://groq.com/) to query LLMs. 

Do `pip install groq`
Follow `https://console.groq.com/keys` to create a free account and get an API key

The backend uses NewsAPI to source some articles. 

Get an API key [here](https://newsapi.org/).

## Usage

Copy the environment template:
In a bash termial do : `cp apikey.env.template apikey.env`

Add your own API keys to `apikey.env`.

Do `chmod +x start.sh`

and then run `./start.sh`

