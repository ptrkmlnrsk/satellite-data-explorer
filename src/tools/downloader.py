from pathlib import Path

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.tools.gee_utils import S2Downloader
from src.config import S2Config

import ee


class SentinelDownloader:
    def __init__(self, collection):
        self.collection = collection
        self.image_system_id: str = None

    def set_system_id(
            self, roi: ee.Geometry, start_date: str, end_date: str
    ) -> None:
        """
        Set system_id based on collection.
        """
        # Filter collections
        collection = (
            ee.ImageCollection(self.collection)
            .filterBounds(roi)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", CLOUDY_PIXEL_PERCENTAGE))
        )

        if collection.size().getInfo() == 0:
            raise Exception("Invalid collection")

        # sort based on clouds filtration
        img = collection.sort("CLOUDY_PIXEL_PERCENTAGE").first()

        self.image_system_id = img.get("system:id").getInfo()

    def get_metadata_for_image(self) -> dict[str, str]:
        """
        Get metadata from image system id
        :return: dictionary
        """
        img = ee.Image(self.image_system_id)
        metadata = img.toDictionary().getInfo()

        acquired_at = datetime.fromtimestamp(
            metadata.get("GENERATION_TIME") / 1000, tz=timezone.utc
        ).isoformat()

        return {
            "image_id": self.image_system_id,
            "product_id": metadata.get("PRODUCT_ID"),
            "acquired_at": acquired_at,
            "cloud_pct": metadata.get("CLOUDY_PIXEL_PERCENTAGE"),
            "mgrs_tile": metadata.get("MGRS_TILE"),
            "platform": metadata.get("SPACECRAFT_NAME"),
            "processing_baseline": metadata.get("PROCESSING_BASELINE"),
            "processing_level": metadata.get("PROCESSING_LEVEL"),
            "product_type": metadata.get("PRODUCT_TYPE"),
        }


if __name__ == "__main__":
    # Google Auth
    credentials = authenticate_google_api()
    # Engine init
    initialize_earth_engine(credentials)

    # some configs
    s2_config = SentinelConfig(
        collection="COPERNICUS/S2_SR_HARMONIZED",
        bands=["B4", "B3", "B2", "B8"],
        roi_coordinates=[22.229681, 50.554120],
    )

    roi = get_bounds_from_coordinates(buffer_m=350, s2_config=s2_config.roi_coordinates)

    s2_downloader = SentinelDownloader(s2_config.collection)
    s2_downloader.set_system_id(
        roi=roi, start_date="2022-04-01", end_date="2022-05-30"
    )
    scene_metadata = s2_downloader.get_metadata_for_image()

    image_id = scene_metadata.get("image_id")

    # todo: niezbyt zoptymalizowane, lepiej by bylo wrzucic ten slownik spowrotem
    # todo: do exportera bo odpytywanie klucza tutaj wygląda żałośnie

    product_id = scene_metadata.get("product_id")

    exporter = Exporter(s2_config.bands)
    exporter.export_geotiff(
        image_id=image_id, image_roi=roi, product_id=product_id
    )
