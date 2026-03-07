'''
You will run this problem set from main.py so set things up accordingly
'''
import os
from pathlib import Path

from src.extract import extract_weather_data, extract_transit_data
from src.transform_load import transform_and_load_data


def main():
    api_key = os.getenv("VISUAL_CROSSING_API_KEY")

    if not api_key:
        raise ValueError("Missing API key. Set VISUAL_CROSSING_API_KEY in your terminal first.")

    weather_file = Path("data/weather_data.csv")
    transit_file = Path("data/transit_data.csv")

    if not weather_file.exists():
        extract_weather_data(api_key)
    else:
        print("weather_data.csv already exists, skipping weather extraction.")

    if not transit_file.exists():
        extract_transit_data()
    else:
        print("transit_data.csv already exists, skipping transit extraction.")

    transform_and_load_data()


if __name__ == "__main__":
    main()
    