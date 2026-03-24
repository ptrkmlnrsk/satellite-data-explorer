# TODO to będą operacje na całym rastrze, potrzebne tylko ścieżki
import rasterio
import numpy as np
from typing import Any

RED_BAND = 1
GREEN_BAND = 2
NIR_BAND = 4


def read_raster_bands(file_path: str) -> tuple[Any, Any, Any]:
    with rasterio.open(file_path) as band:
        green_band = band.read(GREEN_BAND).astype("float32")
        red_band = band.read(RED_BAND).astype("float32")
        nir_band = band.read(NIR_BAND).astype("float32")

    return green_band, red_band, nir_band


def denominate_bands(*args):
    return args[0] + args[1]


def write_raster():
    pass


def reproject_raster():
    pass


def generate_mask(*args: Any, **kwargs: Any) -> Any:
    mask = (args[0] == 0) | (args[1] == 0)

    return mask


# TODO te 3 mozna wrzucic do innej klasy bo korzystaja z bandsów
def generate_cir():
    pass


def calculate_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    pass


def calculate_ndwi(green_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    ndwi = np.full(green_band.shape, np.nan)
    denom = denominate_bands(green_band, nir_band)
    return np.divide(green_band - nir_band, denom, out=ndwi, where=denom != 0)

    pass


def generate_stats():
    pass
