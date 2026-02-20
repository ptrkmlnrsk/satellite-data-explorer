from src.authorization.auth import *
import geemap
import ee
import numpy as np

def get_image_info(coordinates: list[float]) -> tuple[str, ee.Geometry]:

    roi = ee.Geometry.Point(coordinates).buffer(250).bounds()

    image = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(roi)
        .filterDate('2025-06-01', '2025-07-30')
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 10))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
        .first()
    )
    full_id = image.get('system:id').getInfo()

    return full_id, roi


def download_image_by_id(image_id: str, output_path: str, image_roi: ee.Geometry) -> None:
    image_to_download = ee.Image(image_id).select(['B4', 'B8', 'B3', 'B2'])

    print(f'Downloading image... {image_to_download}')

    try:
        geemap.ee_export_image(
            image_to_download,
            filename=output_path,
            scale=10,
            region=image_roi,
            file_per_band=False)
        #print('Image has been successfully downloaded to ' + output_path)
    except Exception as e:
        print(e)



if __name__ == "__main__":

    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)

    roi_coordinates = [21.0122, 52.2297]

    img_id, roi = get_image_info(roi_coordinates)


    target_path = f'data/{img_id}.tif'
    print(f'Selected image id: {img_id}')

    if img_id:
        download_image_by_id(image_id=img_id, output_path=target_path, image_roi=roi)
    else:
        print('Image with given parameters has not been found')

