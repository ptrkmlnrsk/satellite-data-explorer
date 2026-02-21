import ee
import geemap
from src.authorization.auth import authenticate_google_api, initialize_earth_engine
import traceback
from datetime import datetime, timezone


def get_pm25(lat: float, lon: float, start_date: str, end_date: str) -> float:
    point = ee.Geometry.Point([lon, lat])
    pm25_collection = (ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
                       .select('Optical_Depth_047')
                       .filterDate(start_date, end_date))
    pm25_mean = (pm25_collection.mean()
                 .reduceRegion(reducer=ee.Reducer.mean(),
                               geometry=point, scale=1000))
    return pm25_mean.getInfo()


def get_image(coordinates: list[float],
                   image_collection: str,
                   start_date: str,
                   end_date: str,
                   cloud_percentage: float | int
                   ) -> tuple[str, ee.Geometry]:

    roi = ee.Geometry.Point(coordinates).buffer(450).bounds()

    image = (
        ee.ImageCollection(image_collection)
        .filterBounds(roi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', cloud_percentage))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
        .first()
    )
    full_id = image.get('system:id').getInfo()

    return full_id, roi


def get_metadata(image_id: str) -> dict[str, str]:
    img = ee.Image(image_id)
    metadata = img.toDictionary().getInfo()

    acquired_at = (
        datetime.fromtimestamp(
            metadata.get('GENERATION_TIME')/1000,tz=timezone.utc)
        .isoformat()
    )

    return {
        "system_id": image_id,
        "acquired_at": acquired_at,
        "cloud_pct": metadata.get("CLOUDY_PIXEL_PERCENTAGE"),
        "mgrs_tile": metadata.get("MGRS_TILE"),
        "product_id": metadata.get("PRODUCT_ID"),
        "platform": metadata.get("SPACECRAFT_NAME"),
        "processing_baseline": metadata.get("PROCESSING_BASELINE"),
    }


def download_image_by_id(image_id: str,
                         output_path: str,
                         image_roi: ee.Geometry) -> None:
    image_to_download = (ee.Image(image_id)
                         .select(['B4', 'B3', 'B2', 'B8'])
                         .clip(image_roi))

    print(f'Downloading image... {image_to_download}')

    try:
        geemap.ee_export_image(
            image_to_download,
            filename=output_path,
            scale=10,
            region=image_roi,
            file_per_band=False)

        print('Image has been successfully downloaded to ' + output_path)

    except Exception as e:
        traceback.print_exc()