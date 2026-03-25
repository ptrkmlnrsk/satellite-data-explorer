import numpy as np


def generate_stats(data: np.ndarray) -> dict:
    return {
        "min": float(np.nanmin(data)),
        "max": float(np.nanmax(data)),
        "mean": float(np.nanmean(data)),
        "nan_ratio": float(np.isnan(data).sum() / data.size * 100),
        "valid_pixels": float(np.isfinite(data)),
    }


# TODO potem dorobić jakieś warunki, które to wszystko sprawdzają
