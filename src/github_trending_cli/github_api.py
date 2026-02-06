import requests

BASE_URL = "https://api.github.com"

def get_api_root() -> dict:
    r = requests.get(BASE_URL,timeout=10)
    r.raise_for_status()
    return r.json()
