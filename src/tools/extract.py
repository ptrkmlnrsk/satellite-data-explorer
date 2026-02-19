from src.authorization.auth import *
import geemap
import ee
import numpy as np

def get_image(coords: list[float]) -> ee.Image:

    point = ee.Geometry.Point(coords[0], coords[1])

    image = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(point)
        .filterDate('2025-06-01', '2025-07-30')
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 10))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
        .first()
    )
    info = image.get('system:index').getInfo()
    return info

if __name__ == "__main__":

    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)

    #result = get_image([21.0122, 52.2297])
    #geemap.ee_export_image(result, filename='sentinel2.tif', scale=10)
    #print(f'Image downloaded: {result}')