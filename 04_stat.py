import os
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Load datasets
# --------------------------------------------------

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

os.makedirs("plots", exist_ok=True)

# --------------------------------------------------
# Split months
# --------------------------------------------------

april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land  = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh  = era5.sel(valid_time=era5.valid_time.dt.month == 7)

# --------------------------------------------------
# Compute monthly spatial averages
# --------------------------------------------------

def compute_stats(land_ds, blh_ds):

    rain = land_ds["tp"].mean().item() * 1000          # mm
    soil = land_ds["swvl1"].mean().item()              # m3/m3
    temp = land_ds["t2m"].mean().item() - 273.15       # °C
    blh  = blh_ds["blh"].mean().item()                 # m

    return rain, soil, temp, blh


apr = compute_stats(april_land, april_blh)
jul = compute_stats(july_land, july_blh)

# --------------------------------------------------
# Create dataframe
# --------------------------------------------------

summary = pd.DataFrame({

    "Variable":[
        "Rainfall (mm)",
        "Soil Moisture",
        "Temperature (°C)",
        "Boundary Layer Height (m)"
    ],

    "April":[
        apr[0],
        apr[1],
        apr[2],
        apr[3]
    ],

    "July":[
        jul[0],
        jul[1],
        jul[2],
        jul[3]
    ]

})

summary["Difference"] = summary["July"] - summary["April"]

summary["% Change"] = (
    summary["Difference"] /
    summary["April"]
) * 100

print(summary)

summary.to_csv(
    "plots/seasonal_summary.csv",
    index=False
)

# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, ax = plt.subplots(2,2, figsize=(11,8))

variables = [
    "Rainfall (mm)",
    "Soil Moisture",
    "Temperature (°C)",
    "Boundary Layer Height (m)"
]

for i, variable in enumerate(variables):

    r = i // 2
    c = i % 2

    april = summary.loc[
        summary["Variable"]==variable,
        "April"
    ].values[0]

    july = summary.loc[
        summary["Variable"]==variable,
        "July"
    ].values[0]

    ax[r,c].bar(
        ["April","July"],
        [april,july]
    )

    ax[r,c].set_title(variable)

plt.suptitle(
    "Seasonal Comparison (April vs July)",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "plots/Figure2_Seasonal_Statistics.png",
    dpi=300
)

plt.savefig(
    "plots/Figure2_Seasonal_Statistics.pdf"
)

plt.show()