import xarray as xr

ds = xr.open_dataset("era5land_kerala_may2024.nc")

print(ds)
print("\nVariables:")
print(list(ds.data_vars))