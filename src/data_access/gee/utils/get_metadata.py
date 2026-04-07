from ee import Image
from datetime import datetime, timezone

from src.domain.metadata import ImageMetadata


def get_gee_metadata_of_image(image_system_id: str) -> ImageMetadata:
    """
    Extracts particular metadata of image to a dictionary and provides
    with necessary data of image.
    :return: dictionary
    """
    img = Image(image_system_id)
    metadata = img.toDictionary().getInfo()

    acquired_at = datetime.fromtimestamp(
        metadata.get("GENERATION_TIME") / 1000, tz=timezone.utc
    ).isoformat()

    return ImageMetadata(
        image_id=image_system_id,
        product_id=metadata.get("PRODUCT_ID"),
        acquired_at=acquired_at,
        cloud_pct=metadata.get("CLOUDY_PIXEL_PERCENTAGE"),
        mgrs_tile=metadata.get("MGRS_TILE"),
        platform=metadata.get("SPACECRAFT_NAME"),
        processing_baseline=metadata.get("PROCESSING_BASELINE"),
        processing_level=metadata.get("PROCESSING_LEVEL"),
        product_type=metadata.get("PRODUCT_TYPE"),
    )
