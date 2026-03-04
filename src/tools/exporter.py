from ee import Image, Geometry
from traceback import print_exc
from geemap import ee_export_image

from src.tools.constants import DATA_DIR

class Exporter:
    def __init__(self, bands: list[str]):
        self.bands = bands

    def export_geotiff(
            self, image_id: str, image_roi: Geometry, product_id: str
    ) -> None:
        # bands
        image_to_download = Image(image_id).select(self.bands).clip(image_roi)

        safe_id = product_id.replace("/", "_")
        output_name = DATA_DIR / f"{safe_id}.tif"

        print(f"Downloading image... {image_to_download}")

        try:
            ee_export_image(
                image_to_download,
                filename=str(output_name),
                scale=10,
                region=image_roi,
                file_per_band=False,
            )

            print("Image has been successfully downloaded to ", DATA_DIR)

        except Exception:
            print_exc()
