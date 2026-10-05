import pandas as pd
import requests


url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=27.7172&longitude=85.3240"
    "&hourly=temperature_2m,relative_humidity_2m"
)

response = requests.get(url, timeout=30)
response.raise_for_status()
data = response.json()

df = pd.DataFrame(
    {
        "timestamp": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
    }
)

df.to_csv("raw_weather_data.csv", index=False)
print(f"Data extracted successfully! Saved {len(df)} rows.")
