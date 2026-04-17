import os
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

import requests


API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")


def get_forecast():
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not set.")
    if not LAT or not LON:
        raise ValueError("LAT and LON must be set.")

    current_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": LAT,
        "lon": LON,
        "units": "imperial",
        "appid": API_KEY,
    }

    current_response = requests.get(current_url, params=params, timeout=20)
    current_response.raise_for_status()
    current_data = current_response.json()

    forecast_response = requests.get(forecast_url, params=params, timeout=20)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    ny_tz = ZoneInfo("America/New_York")
    days = {}

    for entry in forecast_data["list"]:
        dt_utc = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=ZoneInfo("UTC")
        )
        dt_ny = dt_utc.astimezone(ny_tz)
        day = dt_ny.date().isoformat()

        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["main"]

        if day not in days:
            days[day] = {
                "temps": [],
                "conditions": [],
            }

        days[day]["temps"].append(temp)
        days[day]["conditions"].append(condition)

    forecast = []

    for i, day in enumerate(sorted(days.keys())[:6]):
        temps = days[day]["temps"]
        conditions = days[day]["conditions"]

        day_entry = {
            "date": day,
            "high": round(max(temps)),
            "low": round(min(temps)),
            "condition": Counter(conditions).most_common(1)[0][0],
        }

        if i == 0:
            day_entry["current"] = round(current_data["main"]["temp"])

        forecast.append(day_entry)

    return forecast
