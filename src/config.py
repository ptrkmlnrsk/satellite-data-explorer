from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

CLIENT_SECRET_FILE = getenv("CLIENT_SECRET_FILE")
CLIENT_TOKEN_PICKLE_FILE = getenv("CLIENT_TOKEN_PICKLE_FILE")
DATABASE_URL = getenv("DATABASE_URL")

CLOUDY_PIXEL_PERCENTAGE: float = 30


@dataclass
class SentinelConfig:
    """
    Defines image configuration parameters
    """

    collection: str
    bands: list[str]
    roi_coordinates: list[float]
