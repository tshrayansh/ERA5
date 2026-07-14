import xarray as xr

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
era5 = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

april_land = land.sel(valid_time=land.valid_time.dt.month == 4)
july_land  = land.sel(valid_time=land.valid_time.dt.month == 7)

april_blh = era5.sel(valid_time=era5.valid_time.dt.month == 4)
july_blh  = era5.sel(valid_time=era5.valid_time.dt.month == 7)

print("April (Land):", april_land.valid_time.size, "days")
print("July  (Land):", july_land.valid_time.size, "days")

print("April (BLH):", april_blh.valid_time.size, "days")
print("July  (BLH):", july_blh.valid_time.size, "days")


# Monthly mean maps


april_sm = april_land["swvl1"].mean(dim="valid_time")
july_sm  = july_land["swvl1"].mean(dim="valid_time")

april_temp = april_land["t2m"].mean(dim="valid_time") - 273.15
july_temp  = july_land["t2m"].mean(dim="valid_time") - 273.15

april_blh_map = april_blh["blh"].mean(dim="valid_time")
july_blh_map  = july_blh["blh"].mean(dim="valid_time")

print("Monthly mean maps computed.")