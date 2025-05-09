# echochamber

## Usage

Add your own API keys to `apikey.env`.

Do `chmod +x start.sh`

and then run `./start.sh`

## Installation

`classifier.py` uses [Groq](https://groq.com/) to query LLMs.

Follow [this tutorial](https://console.groq.com/docs/quickstart) to get started, which gets you to:
- Sign up for a (free) account
- Create an API key
- Configure your API key as an environment variable, by running
  `export GROQ_API_KEY=<your-api-key-here>`
  > **Warning:** Do **not** push any code or file containing your API key to a GitHub remote repo as this is a secret and must be kept secure!


