import os
import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import ttest_ind

print("="*60)
print("STATISTICS ANALYSIS")
print("="*60)

# ----------------------------------------------------------
# Create output folder
# ----------------------------------------------------------

os.makedirs("plots", exist_ok=True)

# ----------------------------------------------------------
# Load datasets
# ----------------------------------------------------------

print("Loading datasets...")

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

print("Datasets loaded.\n")

# ----------------------------------------------------------
# Split April and July
# ----------------------------------------------------------

april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land  = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh  = era5.sel(valid_time=era5.valid_time.dt.month == 7)

# ----------------------------------------------------------
# Daily spatial averages
# ----------------------------------------------------------

april_rain = april_land["tp"].mean(dim=["latitude","longitude"]).values * 1000
july_rain  = july_land["tp"].mean(dim=["latitude","longitude"]).values * 1000

april_soil = april_land["swvl1"].mean(dim=["latitude","longitude"]).values
july_soil  = july_land["swvl1"].mean(dim=["latitude","longitude"]).values

april_temp = (
    april_land["t2m"]
    .mean(dim=["latitude","longitude"])
    .values
    - 273.15
)

july_temp = (
    july_land["t2m"]
    .mean(dim=["latitude","longitude"])
    .values
    - 273.15
)

april_blh_daily = (
    april_blh["blh"]
    .mean(dim=["latitude","longitude"])
    .values
)

july_blh_daily = (
    july_blh["blh"]
    .mean(dim=["latitude","longitude"])
    .values
)

# ----------------------------------------------------------
# Monthly means
# ----------------------------------------------------------

def monthly_mean(data):
    return float(np.mean(data))

summary = pd.DataFrame({

    "Variable":[
        "Rainfall (mm)",
        "Soil Moisture (m³/m³)",
        "Temperature (°C)",
        "Boundary Layer Height (m)"
    ],

    "April":[
        monthly_mean(april_rain),
        monthly_mean(april_soil),
        monthly_mean(april_temp),
        monthly_mean(april_blh_daily)
    ],

    "July":[
        monthly_mean(july_rain),
        monthly_mean(july_soil),
        monthly_mean(july_temp),
        monthly_mean(july_blh_daily)
    ],

    "April SD":[
        np.std(april_rain),
        np.std(april_soil),
        np.std(april_temp),
        np.std(april_blh_daily)
    ],

    "July SD":[
        np.std(july_rain),
        np.std(july_soil),
        np.std(july_temp),
        np.std(july_blh_daily)
    ]

})

summary["Difference"] = summary["July"] - summary["April"]

summary["Percent Change"] = (
    summary["Difference"] /
    summary["April"]
) * 100

summary = summary.round(3)

# ----------------------------------------------------------
# Statistical Tests
# ----------------------------------------------------------

variables = {

    "Rainfall": (april_rain, july_rain),

    "Soil Moisture": (april_soil, july_soil),

    "Temperature": (april_temp, july_temp),

    "Boundary Layer Height": (
        april_blh_daily,
        july_blh_daily
    )

}

p_values = []

print("\n")
print("="*60)
print("WELCH'S T-TEST")
print("="*60)

for variable, (apr, jul) in variables.items():

    t, p = ttest_ind(
        apr,
        jul,
        equal_var=False,
        nan_policy="omit"
    )

    p_values.append(p)

    print(f"\n{variable}")

    print(f"April Mean : {np.mean(apr):.3f}")
    print(f"July Mean  : {np.mean(jul):.3f}")

    print(f"T statistic : {t:.3f}")
    print(f"P value     : {p:.5f}")

    if p < 0.05:
        print("Result      : Significant")
    else:
        print("Result      : Not Significant")

summary["P-value"] = np.round(p_values,5)

summary["Significant"] = summary["P-value"] < 0.05

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

outfile = "plots/summary_statistics.csv"

summary.to_csv(outfile,index=False)

print("\n")
print("="*60)
print("SUMMARY TABLE")
print("="*60)

print(summary)

print("\n")
print(f"Saved to: {outfile}")

print("\nDone.")