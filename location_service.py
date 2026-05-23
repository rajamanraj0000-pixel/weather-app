import requests
import geocoder

class LocationService:
    @staticmethod
    def get_current_location():
        """Get user's current location using multiple methods"""
        
        # Method 1: Try geocoder library (most reliable)
        try:
            print("🌍 Detecting location with geocoder...")
            g = geocoder.ip('me')
            
            if g.ok and g.city:
                print(f"✓ Location detected: {g.city}, {g.country}")
                return {
                    'city': g.city,
                    'country': g.country,
                    'lat': g.latlng[0],
                    'lon': g.latlng[1]
                }
        except Exception as e:
            print(f"⚠ Geocoder failed: {e}")
        
        # Method 2: ipapi.co
        try:
            print("🌍 Trying ipapi.co...")
            response = requests.get('https://ipapi.co/json/', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('city') and data.get('latitude'):
                    print(f"✓ Location: {data.get('city')}, {data.get('country_name')}")
                    
                    return {
                        'city': data.get('city'),
                        'country': data.get('country_code', 'US'),
                        'lat': float(data.get('latitude')),
                        'lon': float(data.get('longitude'))
                    }
        except Exception as e:
            print(f"⚠ ipapi.co failed: {e}")
        
        # Method 3: ip-api.com
        try:
            print("🌍 Trying ip-api.com...")
            response = requests.get('http://ip-api.com/json/', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    print(f"✓ Location: {data.get('city')}, {data.get('country')}")
                    
                    return {
                        'city': data.get('city'),
                        'country': data.get('countryCode', 'US'),
                        'lat': float(data.get('lat')),
                        'lon': float(data.get('lon'))
                    }
        except Exception as e:
            print(f"⚠ ip-api.com failed: {e}")
        
        # Method 4: ipinfo.io
        try:
            print("🌍 Trying ipinfo.io...")
            response = requests.get('https://ipinfo.io/json', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('city') and data.get('loc'):
                    loc = data.get('loc').split(',')
                    print(f"✓ Location: {data.get('city')}, {data.get('country')}")
                    
                    return {
                        'city': data.get('city'),
                        'country': data.get('country', 'US'),
                        'lat': float(loc[0]),
                        'lon': float(loc[1])
                    }
        except Exception as e:
            print(f"⚠ ipinfo.io failed: {e}")
        
        # Fallback to user's likely location based on timezone/language
        # You can change this to your preferred default city
        print("⚠ Using fallback location")
        
        # Try to detect from browser if possible (this is server-side fallback)
        return {
            'city': 'Mumbai',  # Change to your city
            'country': 'IN',
            'lat': 19.0760,
            'lon': 72.8777
        }
    
    @staticmethod
    def get_location_by_city(city_name):
        """Get coordinates for a city name"""
        from config import Config
        
        try:
            print(f"🔍 Searching for: {city_name}")
            
            url = f"{Config.WEATHER_BASE_URL}/search.json"
            params = {
                'key': Config.WEATHER_API_KEY,
                'q': city_name
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f"City search failed")
            
            data = response.json()
            
            if not data:
                raise Exception(f"City '{city_name}' not found")
            
            result = data[0]
            print(f"✓ Found: {result['name']}, {result['country']}")
            
            return {
                'city': result['name'],
                'country': result['country'],
                'lat': result['lat'],
                'lon': result['lon']
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise