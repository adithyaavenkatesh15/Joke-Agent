import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("JOKES_API_KEY")


def get_joke():

    url = "https://api.api-ninjas.com/v1/jokes"

    headers = {
        "X-Api-Key": API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    joke = response.json()

    return joke[0]["joke"]