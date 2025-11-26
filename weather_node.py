# app/weather_node.py
import os, requests
from dotenv import load_dotenv
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city: str):
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY not set in .env")
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {
        "city": data.get("name"),
        "temp_c": data.get("main", {}).get("temp"),
        "feels_like_c": data.get("main", {}).get("feels_like"),
        "weather": data.get("weather", [{}])[0].get("description"),
        "raw": data
    }

def weather_to_text(w: dict) -> str:
    return f"Weather in {w.get('city')}: {w.get('weather')}. Temp {w.get('temp_c')}°C (feels like {w.get('feels_like_c')}°C)." 
