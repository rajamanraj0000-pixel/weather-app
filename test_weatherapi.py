import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('WEATHER_API_KEY')

if not api_key:
    print("❌ NO API KEY FOUND in .env file!")
    exit()

print(f"✓ API Key loaded: {api_key[:10]}...")

# Test current weather
url = "https://api.weatherapi.com/v1/current.json"
params = {
    'key': api_key,
    'q': 'London'
}

print("\nTesting WeatherAPI.com...")
response = requests.get(url, params=params)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✓ SUCCESS!")
    print(f"Location: {data['location']['name']}, {data['location']['country']}")
    print(f"Temperature: {data['current']['temp_c']}°C")
    print(f"Condition: {data['current']['condition']['text']}")
else:
    print(f"❌ FAILED: {response.json()}")