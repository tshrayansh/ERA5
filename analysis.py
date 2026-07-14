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


# FIGURE 1
# Monthly Mean Maps

fig, ax = plt.subplots(2, 2, figsize=(11, 9))

im1 = april_sm.plot(
    ax=ax[0,0],
    cmap="YlGnBu",
    vmin=sm_min,
    vmax=sm_max,
    add_colorbar=False
)

ax[0,0].set_title("April Soil Moisture")

july_sm.plot(
    ax=ax[0,1],
    cmap="YlGnBu",
    vmin=sm_min,
    vmax=sm_max,
    add_colorbar=False
)

ax[0,1].set_title("July Soil Moisture")

im2 = april_blh_map.plot(
    ax=ax[1,0],
    cmap="plasma",
    vmin=blh_min,
    vmax=blh_max,
    add_colorbar=False
)

ax[1,0].set_title("April BLH")

july_blh_map.plot(
    ax=ax[1,1],
    cmap="plasma",
    vmin=blh_min,
    vmax=blh_max,
    add_colorbar=False
)

ax[1,1].set_title("July BLH")

fig.colorbar(
    im1,
    ax=ax[0,:],
    shrink=0.8,
    label="Soil Moisture (m³/m³)"
)

fig.colorbar(
    im2,
    ax=ax[1,:],
    shrink=0.8,
    label="Boundary Layer Height (m)"
)

plt.tight_layout()

plt.savefig("plots/maps.png", dpi=300)

plt.show()


# FIGURE 2
# Daily Time Series


fig, axs = plt.subplots(
    4,
    1,
    figsize=(12,12),
    sharex=True,
    constrained_layout=True
)

axs[0].bar(
    time,
    rain,
    color="royalblue"
)

axs[0].set_ylabel("Rain (mm)")
axs[0].set_title("Rainfall")

axs[1].plot(
    time,
    soil,
    color="forestgreen",
    linewidth=2
)

axs[1].set_ylabel("m³/m³")
axs[1].set_title("Soil Moisture")

axs[2].plot(
    time,
    temp,
    color="tomato",
    linewidth=2
)

axs[2].set_ylabel("°C")
axs[2].set_title("2 m Temperature")

axs[3].plot(
    time,
    blh,
    color="purple",
    linewidth=2
)

axs[3].set_ylabel("m")
axs[3].set_title("Boundary Layer Height")

axs[3].set_xlabel("Date")

# Show month boundary

for a in axs:
    a.axvline(
        time.values[30],
        linestyle="--",
        color="black",
        alpha=0.5
    )

plt.savefig(
    "plots/Figure2_TimeSeries.png",
    dpi=300
)

plt.close()
# Spatial averages for time series
# ==========================================================

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

# ==========================================================
# FIGURE 2 : TIME SERIES
# ==========================================================

fig, axs = plt.subplots(
    4,
    2,
    figsize=(14,10),
    sharex="col"
)

# ---------------- Rain ----------------

axs[0,0].bar(april_land.valid_time, april_rain, color="royalblue")
axs[0,0].set_title("April")
axs[0,0].set_ylabel("Rain (mm)")

axs[0,1].bar(july_land.valid_time, july_rain, color="royalblue")
axs[0,1].set_title("July")

# ---------------- Soil Moisture ----------------

axs[1,0].plot(april_land.valid_time, april_soil, color="forestgreen", linewidth=2)
axs[1,0].set_ylabel("Soil Moisture")

axs[1,1].plot(july_land.valid_time, july_soil, color="forestgreen", linewidth=2)

# ---------------- Temperature ----------------

axs[2,0].plot(april_land.valid_time, april_temp, color="tomato", linewidth=2)
axs[2,0].set_ylabel("Temp (°C)")

axs[2,1].plot(july_land.valid_time, july_temp, color="tomato", linewidth=2)

# ---------------- BLH ----------------

axs[3,0].plot(april_land.valid_time, april_blh_ts, color="purple", linewidth=2)
axs[3,0].set_ylabel("BLH (m)")
axs[3,0].set_xlabel("Date")

axs[3,1].plot(july_land.valid_time, july_blh_ts, color="purple", linewidth=2)
axs[3,1].set_xlabel("Date")

plt.tight_layout()

plt.savefig("plots/seasonal_timeseries.png", dpi=300)

plt.show()

plt.close()

# ==========================================================
# Print summary
# ==========================================================

print("\n================ APRIL ================")
print(f"Rainfall      : {april_rain.mean().item():.2f} mm")
print(f"Soil Moisture : {april_soil.mean().item():.3f}")
print(f"Temperature   : {april_temp.mean().item():.2f} °C")
print(f"BLH           : {april_blh_ts.mean().item():.2f} m")

print("\n================ JULY ================")
print(f"Rainfall      : {july_rain.mean().item():.2f} mm")
print(f"Soil Moisture : {july_soil.mean().item():.3f}")
print(f"Temperature   : {july_temp.mean().item():.2f} °C")
print(f"BLH           : {july_blh_ts.mean().item():.2f} m")