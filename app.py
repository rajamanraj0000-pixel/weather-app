from flask import Flask, render_template, request, jsonify
from config import Config
from weather_service import WeatherService
from location_service import LocationService

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
try:
    weather_service = WeatherService()
    print("✓ Weather service initialized")
except Exception as e:
    print(f"✗ Failed to initialize: {e}")
    weather_service = None

location_service = LocationService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/current')
def get_current_weather():
    """Get current weather"""
    if not weather_service:
        return jsonify({'error': 'Service not available. Check API key in .env'}), 500
    
    try:
        city = request.args.get('city')
        
        if city:
            location = location_service.get_location_by_city(city)
        else:
            location = location_service.get_current_location()
        
        weather_data = weather_service.get_current_weather(
            location['lat'], 
            location['lon']
        )
        
        if weather_data:
            weather_data['icon_url'] = WeatherService.get_weather_icon_url(
                weather_data['icon']
            )
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'Unable to fetch weather'}), 500
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/forecast')
def get_forecast():
    """Get 5-day forecast"""
    if not weather_service:
        return jsonify({'error': 'Service not available'}), 500
    
    try:
        city = request.args.get('city')
        
        if city:
            location = location_service.get_location_by_city(city)
        else:
            location = location_service.get_current_location()
        
        forecast_data = weather_service.get_forecast(
            location['lat'], 
            location['lon']
        )
        
        if forecast_data:
            for day in forecast_data:
                day['icon_url'] = WeatherService.get_weather_icon_url(day['icon_url'])
            return jsonify(forecast_data)
        else:
            return jsonify({'error': 'Unable to fetch forecast'}), 500
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌤️  WEATHER APP STARTING...")
    print("="*60)
    
    if Config.WEATHER_API_KEY:
        print(f"✓ API Key: {Config.WEATHER_API_KEY[:10]}...")
    else:
        print("✗ NO API KEY! Add WEATHER_API_KEY to .env file")
    
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)