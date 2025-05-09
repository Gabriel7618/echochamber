# echochamber

## API Keys

* The classifier uses [Groq](https://groq.com/) to query LLMs. Follow [Groq key](https://console.groq.com/keys) to create a free account and get an API key

* The backend uses NewsAPI to source some articles. Get an API key [here](https://newsapi.org/).

* The webpage uses node.js to run the local server. Install node.js [here](https://nodejs.org/en)

## Usage

Copy the environment template:
In a bash termial do : `cp apikey.env.template apikey.env`

Add your own API keys to `apikey.env`.

Do `chmod +x start.sh`

and then run `./start.sh`

