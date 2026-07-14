import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-land"

request = {
    "variable": [
        "2m_temperature",
        "total_precipitation",
        "volumetric_soil_water_layer_1"
    ],
    "year": "2024",
    "month": [
        "04",
        "07"
    ],
    "day": [
        "01","02","03","04","05","06","07","08","09","10",
        "11","12","13","14","15","16","17","18","19","20",
        "21","22","23","24","25","26","27","28","29","30"
    ],
    "time": [
        "12:00"
    ],
    "area": [
        12.8,
        74.8,
        8.0,
        77.8
    ],
    "data_format": "netcdf",
    "download_format": "unarchived"
}

client.retrieve(
    dataset,
    request
).download("era5land_kerala_apr_jul_2024.nc")