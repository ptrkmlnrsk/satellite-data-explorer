from dataclasses import dataclass
from datetime import date


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
    collection: str
    start_date: date | None
    end_date: date | None
    coordinates: tuple[float, float]
    # roi: list[list[tuple[float, float]]]
    cloud_cover: float
    #bands: list[str]
    buffer: int = 350

    # @property
    # def roi(self):
    #    if self.roi is None:
    #        return None
    #    return get_bounds_from_coordinates(
    #        roi_coordinates=self.coordinates,
    #        buffer_m=self.buffer)

    # TODO poczytać o property
