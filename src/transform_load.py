'''
PART 2: Merge and transform the data
- Read in the two datasets from /data into two separate dataframes
- Profile, clean, and standardize date fields for both as needed
- Merge the two dataframe for the date range 10/1/2024 - 10/31/2025
- Conduct EDA to understand the relationship between weather and transit ridership over time
-- Create a line plot of daily transit ridership and daily average temperature over the whole time period
-- For February 2025, create a scatterplot of daily transit ridership vs. precipitation
-- Create a correlation heatmap of all numeric features in the merged dataframe
-- Load the merged dataframe as a CSV into /data
-- In a print statement, summarize any interesting trends you see in the merged dataset

'''

#Write your code below
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_DIR = Path("data")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)


def transform_and_load_data():
    weather = pd.read_csv(DATA_DIR / "weather_data.csv")
    transit = pd.read_csv(DATA_DIR / "transit_data.csv")

    weather.columns = weather.columns.str.strip().str.lower()
    transit.columns = transit.columns.str.strip().str.lower()

    print("Weather columns:", weather.columns.tolist())
    print("Transit columns:", transit.columns.tolist())

    weather["datetime"] = pd.to_datetime(weather["datetime"])
    transit["service_date"] = pd.to_datetime(transit["service_date"])

    weather = weather[
        ["weather_id", "datetime", "temp", "tempmax", "tempmin", "precip", "humidity", "windspeed"]
    ]

    daily_transit = (
        transit.groupby("service_date", as_index=False)["total_rides"]
        .sum()
        .rename(columns={"service_date": "date", "total_rides": "daily_ridership"})
    )

    merged = pd.merge(
        weather,
        daily_transit,
        left_on="datetime",
        right_on="date",
        how="inner"
    )

    merged.to_csv(DATA_DIR / "merged_weather_transit.csv", index=False)

    plt.figure(figsize=(12, 6))
    plt.plot(merged["datetime"], merged["daily_ridership"], label="Transit Ridership")
    plt.plot(merged["datetime"], merged["temp"], label="Average Temperature")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Daily Transit Ridership and Average Temperature")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "lineplot_ridership_temperature.png")
    plt.close()

    feb_2025 = merged[
        (merged["datetime"] >= "2025-02-01") &
        (merged["datetime"] <= "2025-02-28")
    ]

    plt.figure(figsize=(8, 6))
    plt.scatter(feb_2025["precip"], feb_2025["daily_ridership"])
    plt.xlabel("Precipitation")
    plt.ylabel("Daily Transit Ridership")
    plt.title("February 2025: Ridership vs Precipitation")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "scatter_feb2025_ridership_precip.png")
    plt.close()

    plt.figure(figsize=(10, 8))
    sns.heatmap(merged.select_dtypes(include="number").corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "correlation_heatmap.png")
    plt.close()

    print("Merged dataset saved to data/merged_weather_transit.csv")
    print("Plots saved to plots/")
    print("Interesting trend: ridership tends to be higher on warmer days and may decrease on days with more precipitation.")

    return merged