import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import json

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json"


def getWeatherForecast(dates, location):
    forecasts = {}

    if not WEATHER_API_KEY:
        return {d: "Unknown" for d in dates}

    for raw_date in dates:
        try:
            date = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            
            params = {
                "key": WEATHER_API_KEY,
                "q": location,
                "dt": date
            }

            response = requests.get(WEATHER_API_URL, params=params, timeout=5)

            response.raise_for_status()

            data = response.json()

            forecast_day = data.get("forecast", {}).get("forecastday", [])
            if forecast_day:
                condition = forecast_day[0]["day"]["condition"]["text"]
            else:
                condition = "Unknown"

            forecasts[raw_date] = condition

        except Exception as e:
            forecasts[raw_date] = "Unknown"

    return forecasts
