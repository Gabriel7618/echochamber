import requests
 
try:

    response = requests.get("http://127.0.0.1:8000/articles/trump")

    response.raise_for_status() 

    data = response.json()

    print("JSON Response:")

    print(data)

except requests.exceptions.RequestException as e:

    print("Request failed:", e)

except ValueError:

    print("Response is not valid JSON.")

