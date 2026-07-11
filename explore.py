import xarray as xr

# Open datasets
land = xr.open_dataset("era5land_kerala_may2024.nc")
blh = xr.open_dataset("era5_blh_kerala_may2024.nc")

print("="*60)
print("ERA5-Land Dataset")
print("="*60)
print(land)

print("\nVariables:")
print(list(land.data_vars))

print("\n")

print("="*60)
print("ERA5 Dataset")
print("="*60)
print(blh)

print("\nVariables:")
print(list(blh.data_vars))