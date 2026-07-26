from pydantic import BaseModel
# from typing import Optional

from src.domain.enums.sentinel2_bands import Sentinel2Band

BANDS_RENAMEED = {}

class GEEImageRequest(BaseModel):
    """
    An object to represent an Earth Engine image request.
    Roi parameter has to be Polygon object with at least 3 vertices.

    :image_id: path to location on GEE storages to particular scene
    :bands: list of bands
    :bands_renamed: new names for bands
    :roi: has to have at least 3 points
    """

    image_id: str
    bands: list[str]
    bands_renamed: list[str] = None  # add mapped dict to set band names
    roi: list[list[tuple[float, float]]] | tuple[float, float]

    @classmethod
    def validate_bands(cls, bands: list[str]):
        return [Sentinel2Band.from_any(b) for b in bands]
