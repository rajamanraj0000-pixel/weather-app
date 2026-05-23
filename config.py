import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_BASE_URL = 'https://api.weatherapi.com/v1'