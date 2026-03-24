import rasterio
import numpy as np

file_path = "D:\\repos\\sentinel_data_downloader\\data\\S2B_MSIL2A_20230705T092559_N0509_R136_T34UEB_20230705T110524.tif"
out_path = "D:\\repos\\sentinel_data_downloader\\data\\S2B_MSIL2A_20230705T092559_N0509_R136_T34UEB_20230705T110524_NDWI.tif"


RED_BAND = 1
GREEN_BAND = 2
NIR_BAND = 4


def get_bands(*args):
    pass


def remove_nans():
    pass


with rasterio.open(file_path) as src:
    # red = src.read(RED_BAND).astype('float32')
    green = src.read(GREEN_BAND).astype("float32")
    nir = src.read(NIR_BAND).astype("float32")

    denom = nir + green

    mask = (green == 0) | (nir == 0) | (denom == 0)

    ndwi = np.full(green.shape, np.nan, dtype="float32")

    np.divide(green - nir, denom, out=ndwi, where=denom != 0)

    profile = src.profile.copy()
    profile.update(dtype="float32", count=1, nodata=np.nan)

    # TODO robić funkcje z każdej rzeczy

    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(ndwi.astype("float32"), indexes=1)
