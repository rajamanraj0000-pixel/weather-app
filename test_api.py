import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENWEATHER_API_KEY')

print(f"API Key loaded: {api_key[:10]}..." if api_key else "API Key NOT loaded!")

# Test API call
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    'q': 'London',
    'appid': api_key,
    'units': 'metric'
}

response = requests.get(url, params=params)
print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")