from dataclasses import dataclass

from ee import Geometry


class ImageRequest:
    image_id: str


@dataclass
class GEEImageRequest(ImageRequest):
    """An object to represent an Earth Engine image request"""

    image_id: str
    roi: Geometry
    bands: list[str]
