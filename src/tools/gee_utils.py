import ee

from src.authorization.auth import authenticate_google_api, initialize_earth_engine

credentials = authenticate_google_api()
initialize_earth_engine(credentials)

def get_pm25(lat: float, lon: float, start_date: str, end_date: str) -> float:
    point = ee.Geometry.Point([lon, lat])
    pm25_collection = (ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
                       .select('Optical_Depth_047')
                       .filterDate(start_date, end_date))
    pm25_mean = (pm25_collection.mean()
                 .reduceRegion(reducer=ee.Reducer.mean(),
                               geometry=point, scale=1000))
    return pm25_mean.getInfo()