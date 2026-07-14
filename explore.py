import xarray as xr

land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
blh = xr.open_dataset("era5_blh_kerala_apr_jul_2024.nc")

print("="*60)
print("ERA5-Land")
print("="*60)
print(land)

print("\nVariables")
print(list(land.data_vars))

print("\nCoordinates")
print(list(land.coords))

print("\n")

print("="*60)
print("ERA5")
print("="*60)
print(blh)

print("\nVariables")
print(list(blh.data_vars))

print("\nCoordinates")
print(list(blh.coords))