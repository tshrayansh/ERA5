import os
import xarray as xr
import matplotlib.pyplot as plt

land = xr.open_dataset("era5land_kerala_may2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_may2024.nc")


soil = land["swvl1"].mean(dim=["latitude", "longitude"])
temp = land["t2m"].mean(dim=["latitude", "longitude"]) - 273.15
rain = land["tp"].mean(dim=["latitude", "longitude"]) * 1000
blh = era5["blh"].mean(dim=["latitude", "longitude"])

time = land["valid_time"].dt.day

plt.figure(figsize=(8,6))
land["swvl1"].isel(valid_time=0).plot(
    cmap="YlGnBu",
    cbar_kwargs={"label":"Volumetric Soil Water (m³/m³)"}
)
plt.title("Soil Moisture (1 May 2024)", fontsize=18, weight="bold")
plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.tight_layout()
plt.savefig("plots/soil_moisture_map.png", dpi=300)
plt.savefig("plots/soil_moisture_map.pdf")
plt.close()

plt.figure(figsize=(8,6))
era5["blh"].isel(valid_time=0).plot(
    cmap="plasma",
    cbar_kwargs={"label":"Boundary Layer Height (m)"}
)
plt.title("Boundary Layer Height (1 May 2024)", fontsize=18, weight="bold")
plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.tight_layout()
plt.savefig("plots/blh_map.png", dpi=300)
plt.savefig("plots/blh_map.pdf")
plt.close()


fig, axs = plt.subplots(
    4,
    1,
    figsize=(12,12),
    sharex=True
)

# Rainfall
axs[0].bar(time.values, rain.values, width=0.8, color="royalblue")
axs[0].set_ylabel("Rain (mm)")
axs[0].set_title("Average Rainfall", fontsize=14, weight="bold")
axs[0].grid(alpha=0.3)

# Soil Moisture
axs[1].plot(
    time,
    soil,
    marker="o",
    linewidth=2.5,
    markersize=6,
    color="forestgreen"
)
axs[1].set_ylabel("m³/m³")
axs[1].set_title("Volumetric Soil Water", fontsize=14, weight="bold")
axs[1].grid(alpha=0.3)

# Temperature
axs[2].plot(
    time,
    temp,
    marker="o",
    linewidth=2.5,
    markersize=6,
    color="tomato"
)
axs[2].set_ylabel("Temperature (°C)")
axs[2].set_title("2 m Air Temperature", fontsize=14, weight="bold")
axs[2].grid(alpha=0.3)

# BLH
axs[3].plot(
    time,
    blh,
    marker="o",
    linewidth=2.5,
    markersize=6,
    color="purple"
)
axs[3].set_ylabel("BLH (m)")
axs[3].set_xlabel("Date")
axs[3].set_title("Boundary Layer Height", fontsize=14, weight="bold")
axs[3].grid(alpha=0.3)
axs[3].set_xticks(time.values)
axs[3].set_xlabel("Day of May")

plt.tight_layout()

plt.savefig("plots/kerala_timeseries.png", dpi=300)
plt.savefig("plots/kerala_timeseries.pdf")

plt.close()


# Correlation 


plt.figure(figsize=(6,5))

plt.scatter(
    soil.values,
    blh.values,
    s=70,
    color="purple"
)

# Regression line
import numpy as np

m, c = np.polyfit(soil.values, blh.values, 1)

x = np.linspace(
    soil.min().item(),
    soil.max().item(),
    100
)

plt.plot(
    x,
    m*x + c,
    color="black",
    linestyle="--"
)

r = soil.to_series().corr(blh.to_series())

plt.title(f"Soil Moisture vs BLH\nCorrelation = {r:.2f}")

plt.xlabel("Mean Soil Moisture (m³/m³)")
plt.ylabel("Mean Boundary Layer Height (m)")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig("plots/soil_vs_blh_correlation.png", dpi=300)
plt.savefig("plots/soil_vs_blh_correlation.pdf")

plt.close()

print("\n # SUMMARY \n")

print(f"Mean Rainfall      : {rain.mean().item():.2f} mm")
print(f"Mean Soil Moisture : {soil.mean().item():.3f} m³/m³")
print(f"Mean Temperature   : {temp.mean().item():.2f} °C")
print(f"Mean BLH           : {blh.mean().item():.2f} m")

print("\nCorrelation (Soil Moisture vs BLH)")
print("----------------------------------")
print(soil.to_series().corr(blh.to_series()))