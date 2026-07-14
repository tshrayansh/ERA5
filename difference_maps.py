import os
import xarray as xr
import matplotlib.pyplot as plt

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh = era5.sel(valid_time=era5.valid_time.dt.month == 7)

april_sm = april_land["swvl1"].mean(dim="valid_time")
july_sm = july_land["swvl1"].mean(dim="valid_time")

april_blh_map = april_blh["blh"].mean(dim="valid_time")
july_blh_map = july_blh["blh"].mean(dim="valid_time")


# Difference maps

soil_difference = july_sm - april_sm

blh_difference = july_blh_map - april_blh_map


# Plot


fig, ax = plt.subplots(1, 2, figsize=(12,5))

soil_difference.plot(
    ax=ax[0],
    cmap="RdBu",
    center=0,
    cbar_kwargs={"label":"Δ Soil Moisture (m³/m³)"}
)

ax[0].set_title("July − April Soil Moisture")

blh_difference.plot(
    ax=ax[1],
    cmap="RdBu",
    center=0,
    cbar_kwargs={"label":"Δ BLH (m)"}
)

ax[1].set_title("July − April Boundary Layer Height")

plt.tight_layout()

plt.savefig(
    "plots/difference_maps.png",
    dpi=300
)

plt.show()