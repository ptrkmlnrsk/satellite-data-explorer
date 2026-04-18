from src.data_access.base.source import ImagerySource
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.domain.query import QueryParameters
from src.domain.image_request import GEEImageRequest
from src.domain.metadata import ImageMetadata
from src.data_access.gee.image_info_service import GEEImageInfoService
from src.data_access.gee.utils.get_metadata import get_gee_metadata_of_image


class GEEImageService(ImagerySource):
    """
    Dedicated pipeline for downloading images from Earth Engine. Combines
    all steps to download particular image
    """

    def __init__(
        self,
        query_parameters: QueryParameters,
        gee_image_info_service: GEEImageInfoService,
        gee_image_downloader: GEEImageDownloader,
    ) -> None:
        self.query_parameters = query_parameters
        self.gee_image_info_service = gee_image_info_service
        self.gee_image_downloader = gee_image_downloader

    def search(self):
        """
        Searches datasets in cloud for images that fulfill criteria defined in parameters
        :return:
        """
        return self.gee_image_info_service.get_image_id()

    def get_metadata(self, image_id: str) -> ImageMetadata:
        """Returns metadata of image"""
        return get_gee_metadata_of_image(image_id)

    def download(self, image_request: GEEImageRequest) -> None:
        """Downloads selected asset."""
        return self.gee_image_downloader.export_geotiff(image_request)
