# Breaking out of the social media echo chamber

## API Keys

* The classifier uses [Groq](https://groq.com/) to query LLMs. Follow [Groq key](https://console.groq.com/keys) to create a free account and get an API key.

* The backend uses NewsAPI to source some articles. Get an API key [here](https://newsapi.org/).

* The webpage uses node.js to run the local server. Install node.js [here](https://nodejs.org/en).

## Usage

1. Copy the environment template: In your terminal do `cp apikey.env.template apikey.env`.

2. Add your own API keys to `apikey.env`.

3. Do `chmod +x start.sh` and then run `./start.sh`.

