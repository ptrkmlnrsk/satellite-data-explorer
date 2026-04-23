# from enum import Enum

# class Sentinel2Bands(Enum):
#    """Enum object for Sentinel 2 bands.
#    10 m resolution bands:
#    B2, B3, B4, B8"""
#
#    BLUE = {"code": "B2", "resolution": 10, "description": "Blue band"}
#    GREEN = "B3"
#    RED = "B4"
#    RED_EDGE_1 = "B5"
#    RED_EDGE_2 = "B6"
#    RED_EDGE_3 = "B7"
#    NIR = "B8"
#    RED_EDGE_4 = "B8A"
#    WATER_VAPOUR = "B9"
#    CIRRUS = "B10"
#    SWIR_1 = "B11"
#    SWIR_2 = "B12"

from enum import Enum


class Sentinel2Band(Enum):
    BLUE = ("B02", 10)
    GREEN = ("B03", 10)
    RED = ("B04", 10)
    NIR = ("B08", 10)
    RED_EDGE = ("B05", 20)

    def __init__(self, code: str, resolution: int):
        self.code = code
        self.resolution = resolution

    @property
    def is_10m(self):
        return self.resolution == 10

    @classmethod
    def bands_10m(cls):
        return [band for band in cls if band.is_10m]

    @classmethod
    def from_any(cls, value: str):
        if value in cls.__members__:  # lista nazw Blue, green itd.
            return cls[value]
        for band in cls:
            if band.code == value:
                return band
        raise ValueError(f"Invalid Sentinel 2 band: {value}")
