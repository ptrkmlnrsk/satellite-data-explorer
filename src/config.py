from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass
from ee import Geometry

load_dotenv()

CLIENT_SECRET_FILE = getenv("CLIENT_SECRET_FILE")
CLIENT_TOKEN_PICKLE_FILE = getenv("CLIENT_TOKEN_PICKLE_FILE")
DATABASE_URL = getenv("DATABASE_URL")

CLOUDY_PIXEL_PERCENTAGE: float = 30


@dataclass
class SatelliteConfig:
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

    collection: str
    bands: list[str]
    roi: list[float] | Geometry
