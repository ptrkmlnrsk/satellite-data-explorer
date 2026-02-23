import ee
import geemap
import traceback
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path


# def get_pm25(lat: float, lon: float, start_date: str, end_date: str) -> float:
#    point = ee.Geometry.Point([lon, lat])
#    pm25_collection = (ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
#                       .select('Optical_Depth_047')
#                       .filterDate(start_date, end_date))
#    pm25_mean = (pm25_collection.mean()
#                 .reduceRegion(reducer=ee.Reducer.mean(),
#                               geometry=point, scale=1000))
#    return pm25_mean.getInfo()


@dataclass
class S2Config:
    datadir: Path | str
    collection: str
    scale: int
    cloud_perc: int
    bands: list[str]
    roi_coordinates: list[float]


class S2Downloader:
    def __init__(self, cfg: S2Config):
        self.cfg = cfg

    def build_roi(self, buffer_m: int) -> ee.Geometry:
        """
        This method creates circular buffer ROI of point that EE converts to bounding box.
        """
        return ee.Geometry.Point(self.cfg.roi_coordinates).buffer(buffer_m).bounds()

    def find_image_id(
        self, roi: ee.Geometry, start_date: str, end_date: str
    ) -> str | None:
        """
        Find image within collection and retrieve scene ID to download it.
        """
        collection = (
            ee.ImageCollection(self.cfg.collection)
            .filterBounds(roi)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", self.cfg.cloud_perc))
        )

        if collection.size().getInfo() == 0:
            return None

        img = collection.sort("CLOUDY_PIXEL_PERCENTAGE").first()
        return img.get("system:id").getInfo()

    @staticmethod
    def get_metadata_from_col_id(image_system_id: str) -> dict[str, str]:
        """
        Get metadata from image system id
        """
        img = ee.Image(image_system_id)
        metadata = img.toDictionary().getInfo()

        acquired_at = datetime.fromtimestamp(
            metadata.get("GENERATION_TIME") / 1000, tz=timezone.utc
        ).isoformat()

        return {
            "image_id": image_system_id,
            "product_id": metadata.get("PRODUCT_ID"),
            "acquired_at": acquired_at,
            "cloud_percent": metadata.get("CLOUDY_PIXEL_PERCENTAGE"),
            "mgrs_tile": metadata.get("MGRS_TILE"),
            "platform": metadata.get("SPACECRAFT_NAME"),
            "processing_baseline": metadata.get("PROCESSING_BASELINE"),
            "processing_level": metadata.get("PROCESSING_LEVEL"),
            "product_type": metadata.get("PRODUCT_TYPE"),
        }

    def export_geotiff(
        self, image_id: str, image_roi: ee.Geometry, product_id: str
    ) -> None:
        """
        Export ee.Image object to geotiff and save it locally
        """

        image_to_download = ee.Image(image_id).select(self.cfg.bands).clip(image_roi)

        safe_id = product_id.replace("/", "_")
        output_name = self.cfg.datadir / f"{safe_id}.tif"

        print(f"Downloading image... {image_to_download}")

        try:
            geemap.ee_export_image(
                image_to_download,
                filename=str(output_name),
                scale=10,
                region=image_roi,
                file_per_band=False,
            )

            print("Image has been successfully downloaded to ", self.cfg.datadir)

        except Exception:
            traceback.print_exc()
