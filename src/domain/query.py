from dataclasses import dataclass
from ee import Geometry


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

    roi: Geometry
    collection: str
    start_date: str
    end_date: str
    cloud_cover: float
    bands: list[str]
    # sensor: str
