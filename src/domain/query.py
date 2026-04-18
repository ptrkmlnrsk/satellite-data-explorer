from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class QueryParameters:
    """
    Defines image configuration parameters.

    User needs to define a collection as a string.
    Available collections are available here:
    https://developers.google.com/earth-engine/datasets
    egz. COPERNICUS/S2_SR_HARMONIZED

    Bands for specified satellite platform
    are defined as a list of strings.

    ROI might be a Point coordinates or Polygon in crs epsg:4326.

    """

    dataset: str  # GEE albo Planetary Engine/AWS
    collection: str | Any  # TODO collection as str enum
    start_date: datetime
    end_date: datetime  # TODO datetime
    coordinates: list[float]
    cloud_cover: float
    bands: list[str]  # TODO bands enum
    buffer: int = 350
    # sensor: str

    # @property
    # def roi(self):
    #    if self.roi is None:
    #        return None
    #    return get_bounds_from_coordinates(
    #        roi_coordinates=self.coordinates,
    #        buffer_m=self.buffer)

    # TODO poczytać o property
