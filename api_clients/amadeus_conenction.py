import requests
from decouple import config

#Connects to the API and returns token
def authorize_connection():

    client_id=config("AMADEUS_API_KEY")
    client_secret=config("AMADEUS_API_SECRET")
    token_url=config("AMADEUS_TOKEN_URL")

    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response=requests.post(token_url, headers=headers, data=data)

    #Check if connection is successful
    if response.status_code == 200:
        token=response.json()["access_token"]
        return token

    return None