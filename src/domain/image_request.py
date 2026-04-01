from dataclasses import dataclass
from ee import Geometry


@dataclass
class SelectedImageRequest:
    """An object to represent an Earth Engine image request"""

    image_id: str
    roi: Geometry
    bands: list[str]
