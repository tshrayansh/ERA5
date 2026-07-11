import cdsapi

dataset = "reanalysis-era5-single-levels"

request = {
    "product_type": ["reanalysis"],
    "variable": [
        "boundary_layer_height"
    ],
    "year": "2024",
    "month": "05",
    "day": [
        "01", "02", "03", "04", "05",
        "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15"
    ],
    "time": [
        "12:00"
    ],
    "area": [
        12.8,   # North
        74.8,   # West
        8.0,    # South
        77.8    # East
    ],
    "data_format": "netcdf",
    "download_format": "unarchived"
}

client = cdsapi.Client()

client.retrieve(
    dataset,
    request
).download("era5_blh_kerala_may2024.nc")