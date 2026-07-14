import os
import xarray as xr
import matplotlib.pyplot as plt



land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")


april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land  = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh  = era5.sel(valid_time=era5.valid_time.dt.month == 7)

april_sm = april_land["swvl1"].mean(dim="valid_time")
july_sm  = july_land["swvl1"].mean(dim="valid_time")

april_blh_map = april_blh["blh"].mean(dim="valid_time")
july_blh_map  = july_blh["blh"].mean(dim="valid_time")


# Plot


fig, ax = plt.subplots(2, 2, figsize=(12, 10))

# ---------------- Soil Moisture ---------------- #

april_sm.plot(
    ax=ax[0,0],
    cmap="YlGnBu",
    add_colorbar=False
)

ax[0,0].set_title("April 2024\nSoil Moisture")

july_sm.plot(
    ax=ax[0,1],
    cmap="YlGnBu",
    add_colorbar=False
)

ax[0,1].set_title("July 2024\nSoil Moisture")

# ---------------- BLH ---------------- #

april_blh_map.plot(
    ax=ax[1,0],
    cmap="plasma",
    add_colorbar=False
)

ax[1,0].set_title("April 2024\nBoundary Layer Height")

july_blh_map.plot(
    ax=ax[1,1],
    cmap="plasma",
    add_colorbar=False
)

ax[1,1].set_title("July 2024\nBoundary Layer Height")



sm = plt.cm.ScalarMappable(cmap="YlGnBu")
sm.set_array([])

blh = plt.cm.ScalarMappable(cmap="plasma")
blh.set_array([])

fig.colorbar(
    sm,
    ax=ax[0,:],
    orientation="horizontal",
    fraction=0.05,
    pad=0.08,
    label="Soil Moisture (m³/m³)"
)

fig.colorbar(
    blh,
    ax=ax[1,:],
    orientation="horizontal",
    fraction=0.05,
    pad=0.08,
    label="Boundary Layer Height (m)"
)

plt.suptitle(
    "Seasonal Comparison of Land Surface Conditions over Kerala",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig("plots/Figure1_Seasonal_Maps.png", dpi=300)
plt.savefig("plots/Figure1_Seasonal_Maps.pdf")

plt.show()