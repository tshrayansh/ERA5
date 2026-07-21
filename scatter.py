import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh = era5.sel(valid_time=era5.valid_time.dt.month == 7)


april_soil = april_land["swvl1"].mean(dim=["latitude","longitude"]).values
july_soil = july_land["swvl1"].mean(dim=["latitude","longitude"]).values

april_blh_ts = april_blh["blh"].mean(dim=["latitude","longitude"]).values
july_blh_ts = july_blh["blh"].mean(dim=["latitude","longitude"]).values


# Pearson Correlation


r_april, p_april = pearsonr(april_soil, april_blh_ts)

r_july, p_july = pearsonr(july_soil, july_blh_ts)

print("\nCorrelation Results")
print("------------------------------")
print(f"April : r = {r_april:.3f}, p = {p_april:.4f}")

if p_april < 0.05:
    print("April correlation is statistically significant.")
else:
    print("April correlation is NOT statistically significant.")

print()

print(f"July  : r = {r_july:.3f}, p = {p_july:.4f}")

if p_july < 0.05:
    print("July correlation is statistically significant.")
else:
    print("July correlation is NOT statistically significant.")

print(f"April Correlation : {r_april:.3f}")
print(f"July Correlation  : {r_july:.3f}")


# Linear regression

m1, c1 = np.polyfit(april_soil, april_blh_ts, 1)
m2, c2 = np.polyfit(july_soil, july_blh_ts, 1)

x1 = np.linspace(april_soil.min(), april_soil.max(),100)
x2 = np.linspace(july_soil.min(), july_soil.max(),100)


# Plot


plt.figure(figsize=(8,6))

# April
plt.scatter(
    april_soil,
    april_blh_ts,
    color="royalblue",
    label=f"April (r = {r_april:.2f})"
)

plt.plot(
    x1,
    m1*x1+c1,
    color="royalblue",
    linestyle="--"
)

# July
plt.scatter(
    july_soil,
    july_blh_ts,
    color="darkorange",
    label=f"July (r = {r_july:.2f})"
)

plt.plot(
    x2,
    m2*x2+c2,
    color="darkorange",
    linestyle="--"
)

plt.xlabel("Mean Soil Moisture (m³/m³)")
plt.ylabel("Mean Boundary Layer Height (m)")

plt.title("Relationship between Soil Moisture and BLH")

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

plt.savefig(
    "plots/scatter_soil_blh.png",
    dpi=300
)

plt.show()


"""
April : r = -0.511, p = 0.0039
April correlation is statistically significant.

July  : r = 0.294, p = 0.1144
July correlation is NOT statistically significant.
April Correlation : -0.511
"""