import logging

from ee import Image
from traceback import print_exc
from geemap import ee_export_image

from src.tools.constants import DATA_DIR
from src.domain.image_request import GEEImageRequest
from src.api.schemas.polygon_model import GEEPolygon

logger = logging.getLogger(__name__)


class GEEImageDownloader:
    """
    Object that represents an Earth Engine image downloader.
    Requires GEEImageRequest object.
    """

    def export_geotiff(self, selected_image: GEEImageRequest) -> None:
        """
        Downloads image based on provided image_id, list of bands and roi within
        SelectedImageRequest object.
        :param selected_image:
        :param image_id:
        :param bands:
        :param roi:
        :return:
        """

        gee_polygon = GEEPolygon.from_request(selected_image)

        """
        Zmienione w requestcie to w jaki sposob wspolrzedne w slowniku
        zaminieniają się na ROI. Dodano mozliwosc wrzucenia jako tuple i
        list koordynatow jako poligon. Do sprawdzenia czy zadziała.
        """
        image_to_download = (
            Image(selected_image.image_id)
            .select(selectors=selected_image.bands, names=selected_image.bands_renamed)
            # TODO nazwy bandów nie zapisują się do rasterio descriptions
            .clip(gee_polygon)
        )

        safe_id = selected_image.image_id.replace("/", "_")
        output_name = DATA_DIR / f"{safe_id}.tif"

        logger.info(
            "Download image. image_id=%s output=%s bands=%s",
            selected_image.image_id,
            output_name,
            selected_image.bands,
        )

        try:
            ee_export_image(
                image_to_download,
                filename=str(output_name),
                scale=10,
                region=gee_polygon,
                file_per_band=False,
            )

        except Exception:
            print_exc()

        # print("Image has been successfully downloaded to ", DATA_DIR)
