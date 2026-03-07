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


def transform_and_load_data() -> pd.DataFrame:
    
    weather = pd.read_csv(DATA_DIR / "weather_data.csv")
    transit = pd.read_csv(DATA_DIR / "transit_data.csv")

    weather.columns = weather.columns.str.strip().str.lower()
    transit.columns = transit.columns.str.strip().str.lower()


    weather["datetime"] = pd.to_datetime(weather["datetime"], errors="coerce")
    transit["service_date"] = pd.to_datetime(transit["service_date"], errors="coerce")

    weather = weather[
        [
            "weather_id",
            "datetime",
            "temp",
            "tempmax",
            "tempmin",
            "precip",
            "humidity",
            "windspeed",
        ]
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
        how="inner",
    )

    #unique ID to merged output
    merged.insert(0, "merged_id", range(1, len(merged) + 1))

    #merged CSV
    merged_output = DATA_DIR / "merged_weather_transit.csv"
    merged.to_csv(merged_output, index=False)

    #plot 1
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(
        merged["datetime"],
        merged["daily_ridership"],
        label="Transit Ridership",
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Daily Transit Ridership")

    ax2 = ax1.twinx()
    ax2.plot(
        merged["datetime"],
        merged["temp"],
        label="Average Temperature",
    )
    ax2.set_ylabel("Average Temperature (°F)")

    fig.suptitle("Daily Transit Ridership and Average Temperature")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(PLOTS_DIR / "lineplot_ridership_temperature.png")
    plt.close()

    #plot 2
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

    
    #plot 3
    corr_df = merged.drop(columns=["date","merged_id","weather_id"]).select_dtypes(include="number")

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "correlation_heatmap.png")
    plt.close()

    #summary insights
    temp_corr = merged["daily_ridership"].corr(merged["temp"])
    precip_corr = merged["daily_ridership"].corr(merged["precip"])

    print(f"Merged dataset saved to {merged_output}")
    print(f"Plots saved to {PLOTS_DIR}/")
    print(
        f"Ridership has a modest positive correlation with temperature "
        f"({temp_corr:.2f}) and almost no relationship with precipitation "
        f"({precip_corr:.2f})."
    )
    print(
        "Overall, ridership appears to increase on warmer days, while "
        "precipitation does not show a strong daily relationship with ridership."
    )

    return merged