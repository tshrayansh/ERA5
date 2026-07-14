import os
import xarray as xr
import matplotlib.pyplot as plt


land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")



april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh = era5.sel(valid_time=era5.valid_time.dt.month == 7)



april_rain = april_land["tp"].mean(dim=["latitude","longitude"]) * 1000
july_rain = july_land["tp"].mean(dim=["latitude","longitude"]) * 1000

april_soil = april_land["swvl1"].mean(dim=["latitude","longitude"])
july_soil = july_land["swvl1"].mean(dim=["latitude","longitude"])

april_temp = april_land["t2m"].mean(dim=["latitude","longitude"]) - 273.15
july_temp = july_land["t2m"].mean(dim=["latitude","longitude"]) - 273.15

april_blh_ts = april_blh["blh"].mean(dim=["latitude","longitude"])
july_blh_ts = july_blh["blh"].mean(dim=["latitude","longitude"])

pip install scipy

fig, ax = plt.subplots(2,2, figsize=(10,8))

# Rainfall
ax[0,0].boxplot(
    [april_rain.values, july_rain.values],
    tick_labels=["April","July"]
)
ax[0,0].set_title("Rainfall")
ax[0,0].set_ylabel("mm")

# Soil Moisture
ax[0,1].boxplot(
    [april_soil.values, july_soil.values],
    tick_labels=["April","July"]
)
ax[0,1].set_title("Soil Moisture")
ax[0,1].set_ylabel("m³/m³")

# Temperature
ax[1,0].boxplot(
    [april_temp.values, july_temp.values],
    tick_labels=["April","July"]
)
ax[1,0].set_title("2 m Temperature")
ax[1,0].set_ylabel("°C")

# BLH
ax[1,1].boxplot(
    [april_blh_ts.values, july_blh_ts.values],
    tick_labels=["April","July"]
)
ax[1,1].set_title("Boundary Layer Height")
ax[1,1].set_ylabel("m")

plt.suptitle(
    "Distribution of Daily Mean Variables",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "plots/boxplots.png",
    dpi=300
)

plt.show()