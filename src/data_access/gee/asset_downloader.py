from ee import Image
from traceback import print_exc
from geemap import ee_export_image

from src.tools.constants import DATA_DIR
from src.domain.image_request import SelectedImageRequest


class GEEImageDownloader:
    """
    Object that represents an Earth Engine image downloader.
    Requires SelectedImageRequest object.
    """

    def __init__(self, selected_image: SelectedImageRequest) -> None:
        self.selected_image = selected_image

    def export_geotiff(self) -> None:
        """
        Downloads image based on provided image_id, list of bands and roi within
        SelectedImageRequest object.
        :param self:
        :param image_id:
        :param bands:
        :param roi:
        :return:
        """
        image_to_download = (
            Image(self.selected_image.image_id)
            .select(self.selected_image.bands)
            .clip(self.selected_image.roi)
        )

        safe_id = self.selected_image.image_id.replace("/", "_")
        output_name = DATA_DIR / f"{safe_id}.tif"

        print(f"Downloading image... {image_to_download}")

        try:
            ee_export_image(
                image_to_download,
                filename=str(output_name),
                scale=10,
                region=self.selected_image.roi,
                file_per_band=False,
            )

            print("Image has been successfully downloaded to ", DATA_DIR)

        except Exception:
            print_exc()
