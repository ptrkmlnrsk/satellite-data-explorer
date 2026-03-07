from datetime import datetime, timezone
from src.config import CLOUDY_PIXEL_PERCENTAGE

from ee import Geometry, ImageCollection, Filter, Image


class SentinelDownloader:
    def __init__(self, collection):
        self.collection = collection
        self.image_system_id: str = None

    def set_system_id(self, roi: Geometry, start_date: str, end_date: str) -> None:
        """
        Set system_id based on collection.
        """
        # Filter collections
        collection = (
            ImageCollection(self.collection)
            .filterBounds(roi)
            .filterDate(start_date, end_date)
            .filter(Filter.lte("CLOUDY_PIXEL_PERCENTAGE", CLOUDY_PIXEL_PERCENTAGE))
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
        img = Image(self.image_system_id)
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
