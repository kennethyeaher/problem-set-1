'''
PART 1: EXTRACT WEATHER AND TRANSIT DATA

Pull in data from two dataset
1. Weather data from visualcrossing's weather API (https://www.visualcrossing.com/weather-api)
- You will need to sign up for a free account to get an API key
-- You only get 1000 rows free per day, so be careful to build your query correctly up front
-- Though not best practice, include your API key directly in your code for this assignment
- Write code below to get weather data for Chicago, IL for the date range 10/1/2024 - 10/31/2025
- The default data fields should be sufficient
2. Daily transit ridership data for the Chicago Transit Authority (CTA)
- Here is the URL: ttps://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

Load both as CSVs into /data
- Make sure your code is line with the standards we're using in this class 
'''

#Write your code below
import pandas as pd
import requests
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# Extract visual crossing weather data for Chicago, IL

def extract_weather_data(api_key: str) -> pd.DataFrame:
    url = (
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        "Chicago,IL/2024-10-01/2025-10-31"
        f"?unitGroup=us&include=days&key={api_key}&contentType=json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    weather_json = response.json()

    weather_df = pd.DataFrame(weather_json["days"])

    weather_df.insert(0, "weather_id", range(1, len(weather_df) + 1))

    weather_df.to_csv(DATA_DIR / "weather_data.csv", index=False)

    print("Saved weather_data.csv")

    return weather_df



# Extract CTA transit ridership data

def extract_transit_data() -> pd.DataFrame:
    transit_url = (
        "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"
    )

    transit_df = pd.read_csv(transit_url)

    transit_df.insert(0, "transit_id", range(1, len(transit_df) + 1))

    transit_df.to_csv(DATA_DIR / "transit_data.csv", index=False)

    print("Saved transit_data.csv")

    return transit_df