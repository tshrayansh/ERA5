import os
import xarray as xr
import matplotlib.pyplot as plt

# Load datasets


land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")


# Daily spatial averages


soil = land["swvl1"].mean(dim=["latitude", "longitude"])

temp = (
    land["t2m"]
    .mean(dim=["latitude", "longitude"])
    - 273.15
)

rain = (
    land["tp"]
    .mean(dim=["latitude", "longitude"])
    * 1000
)

blh = era5["blh"].mean(dim=["latitude", "longitude"])

time = land["valid_time"]


# Split months


april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh = era5.sel(valid_time=era5.valid_time.dt.month == 7)


# Monthly mean maps


april_sm = april_land["swvl1"].mean(dim="valid_time")
july_sm = july_land["swvl1"].mean(dim="valid_time")

april_blh_map = april_blh["blh"].mean(dim="valid_time")
july_blh_map = july_blh["blh"].mean(dim="valid_time")


# COMMON COLOUR SCALE


sm_min = min(april_sm.min().item(), july_sm.min().item())
sm_max = max(april_sm.max().item(), july_sm.max().item())

blh_min = min(april_blh_map.min().item(), july_blh_map.min().item())
blh_max = max(april_blh_map.max().item(), july_blh_map.max().item())



# Spatial averages for time series

# April

april_rain = april_land["tp"].mean(dim=["latitude","longitude"]) * 1000
april_soil = april_land["swvl1"].mean(dim=["latitude","longitude"])
april_temp = april_land["t2m"].mean(dim=["latitude","longitude"]) - 273.15
april_blh_ts = april_blh["blh"].mean(dim=["latitude","longitude"])

# July

july_rain = july_land["tp"].mean(dim=["latitude","longitude"]) * 1000
july_soil = july_land["swvl1"].mean(dim=["latitude","longitude"])
july_temp = july_land["t2m"].mean(dim=["latitude","longitude"]) - 273.15
july_blh_ts = july_blh["blh"].mean(dim=["latitude","longitude"])


# TIME SERIES: APRIL VS JULY

april_days = april_land.valid_time.dt.day.values
july_days = july_land.valid_time.dt.day.values

fig, axs = plt.subplots(
    4,
    2,
    figsize=(14, 10),
    sharex="col",
    sharey="row"    
)

# ---------------- Rainfall ----------------

axs[0,0].bar(
    april_days,
    april_rain,
    color="royalblue"
)

axs[0,0].set_title("April")
axs[0,0].set_ylabel("Rain (mm)")


axs[0,1].bar(
    july_days,
    july_rain,
    color="royalblue"
)

axs[0,1].set_title("July")


# ---------------- Soil Moisture ----------------

axs[1,0].plot(
    april_days,
    april_soil,
    color="forestgreen",
    linewidth=2
)

axs[1,0].set_ylabel("Soil Moisture (m³/m³)")


axs[1,1].plot(
    july_days,
    july_soil,
    color="forestgreen",
    linewidth=2
)


# ---------------- Temperature ----------------

axs[2,0].plot(
    april_days,
    april_temp,
    color="tomato",
    linewidth=2
)

axs[2,0].set_ylabel("Temperature (°C)")


axs[2,1].plot(
    july_days,
    july_temp,
    color="tomato",
    linewidth=2
)


# ---------------- Boundary Layer Height ----------------

axs[3,0].plot(
    april_days,
    april_blh_ts,
    color="purple",
    linewidth=2
)

axs[3,0].set_ylabel("BLH (m)")
axs[3,0].set_xlabel("Day of Month")


axs[3,1].plot(
    july_days,
    july_blh_ts,
    color="purple",
    linewidth=2
)

axs[3,1].set_xlabel("Day of Month")


for ax in axs.flat:
    ax.set_xticks(range(1, 32, 2))
    ax.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "plots/seasonal_timeseries.png",
    dpi=300)

plt.show()
plt.close()



print("\n APRIL")
print(f"Rainfall      : {april_rain.mean().item():.2f} mm")
print(f"Soil Moisture : {april_soil.mean().item():.3f}")
print(f"Temperature   : {april_temp.mean().item():.2f} °C")
print(f"BLH           : {april_blh_ts.mean().item():.2f} m")

print("\n JULY")
print(f"Rainfall      : {july_rain.mean().item():.2f} mm")
print(f"Soil Moisture : {july_soil.mean().item():.3f}")
print(f"Temperature   : {july_temp.mean().item():.2f} °C")
print(f"BLH           : {july_blh_ts.mean().item():.2f} m")