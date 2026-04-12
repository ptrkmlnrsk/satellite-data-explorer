from dataclasses import dataclass
from datetime import datetime

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

    dataset: str  # GEE albo Planetary Engine/AWS
    roi: Geometry
    collection: str  # TODO collection as str enum
    start_date: datetime
    end_date: datetime  # TODO datetime
    cloud_cover: float
    bands: list[str]  # TODO bands enum
    # sensor: str
