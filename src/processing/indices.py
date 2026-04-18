# TODO to będą operacje na całym rastrze, potrzebne tylko ścieżki
import numpy as np
from typing import Any


def reproject_raster():
    pass


def denominate_bands(*args):
    return args[0] + args[1]


def generate_mask(*args: Any, **kwargs: Any) -> Any:
    mask = (args[0] == 0) | (args[1] == 0)

    return mask


# TODO te 3 mozna wrzucic do innej klasy bo korzystaja z bandsów
def generate_cir():
    pass


def calculate_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    ndvi = np.full(red_band.shape, np.nan)
    denom = denominate_bands(red_band, nir_band)
    return np.divide(red_band - nir_band, denom, out=ndvi, where=denom != 0)


def calculate_ndwi(green_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    ndwi = np.full(green_band.shape, np.nan)
    denom = denominate_bands(green_band, nir_band)
    return np.divide(green_band - nir_band, denom, out=ndwi, where=denom != 0)
