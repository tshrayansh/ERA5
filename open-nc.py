import xarray as xr
land = xr.open_dataset("era5land_kerala_apr_jul_2024.nc")
df = land.to_dataframe().reset_index()
df.to_csv("era5land_kerala_apr_jul_2024.csv", index=False)
print(df.head())
print("\nCSV saved successfully!")