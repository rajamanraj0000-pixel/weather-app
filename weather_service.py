import requests
from datetime import datetime

class WeatherService:
    def __init__(self):
        from config import Config
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_BASE_URL
        
        if not self.api_key:
            raise ValueError("Please set WEATHER_API_KEY in .env file")
    
    def get_current_weather(self, lat, lon):
        """Get current weather data"""
        try:
            url = f"{self.base_url}/current.json"
            params = {
                'key': self.api_key,
                'q': f"{lat},{lon}",
                'aqi': 'no'
            }
            
            print(f"Requesting weather for: {lat},{lon}")
            response = requests.get(url, params=params, timeout=10)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 403:
                raise Exception("Invalid API Key - Please check your WeatherAPI key")
            
            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code}")
            
            data = response.json()
            
            # Get sunrise/sunset from astronomy API
            astro_url = f"{self.base_url}/astronomy.json"
            astro_params = {
                'key': self.api_key,
                'q': f"{lat},{lon}",
                'dt': datetime.now().strftime('%Y-%m-%d')
            }
            astro_response = requests.get(astro_url, params=astro_params, timeout=10)
            astro_data = astro_response.json() if astro_response.status_code == 200 else None
            
            sunrise = "N/A"
            sunset = "N/A"
            
            if astro_data and 'astronomy' in astro_data:
                sunrise = astro_data['astronomy']['astro']['sunrise']
                sunset = astro_data['astronomy']['astro']['sunset']
            
            return {
                'temperature': round(data['current']['temp_c']),
                'feels_like': round(data['current']['feelslike_c']),
                'description': data['current']['condition']['text'],
                'icon': 'https:' + data['current']['condition']['icon'],
                'humidity': data['current']['humidity'],
                'pressure': round(data['current']['pressure_mb']),
                'wind_speed': round(data['current']['wind_kph'], 1),
                'visibility': round(data['current']['vis_km'], 1),
                'sunrise': sunrise,
                'sunset': sunset,
                'city': data['location']['name'],
                'country': data['location']['country']
            }
            
        except Exception as e:
            print(f"Weather API error: {e}")
            raise
    
    def get_forecast(self, lat, lon):
        """Get 5-day forecast"""
        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': f"{lat},{lon}",
                'days': 5,
                'aqi': 'no'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 403:
                raise Exception("Invalid API Key")
            
            if response.status_code != 200:
                raise Exception(f"Forecast API Error: {response.status_code}")
            
            data = response.json()
            forecast_list = []
            
            for day in data['forecast']['forecastday']:
                forecast_list.append({
                    'date': datetime.strptime(day['date'], '%Y-%m-%d').strftime('%a, %b %d'),
                    'temp_min': round(day['day']['mintemp_c']),
                    'temp_max': round(day['day']['maxtemp_c']),
                    'description': day['day']['condition']['text'],
                    'icon': day['day']['condition']['icon'],
                    'icon_url': 'https:' + day['day']['condition']['icon'],
                    'humidity': day['day']['avghumidity']
                })
            
            return forecast_list
            
        except Exception as e:
            print(f"Forecast error: {e}")
            raise
    
    @staticmethod
    def get_weather_icon_url(icon_code):
        """Get weather icon URL"""
        if icon_code.startswith('http'):
            return icon_code
        return 'https:' + icon_code