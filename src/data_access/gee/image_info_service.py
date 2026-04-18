from ee import ImageCollection, Filter, Geometry

from src.domain.query import QueryParameters
from src.data_access.gee.utils.roi_generator import get_bounds_from_coordinates


class GEEImageInfoService:
    """
    Gets parameters from QueryParameters object and returns asset system id
    and metadata
    """

    def __init__(self, query_params: QueryParameters):
        self.query_params = query_params

    def build_gee_roi(self) -> Geometry | None:
        if self.query_params.coordinates is None:
            return None
        return get_bounds_from_coordinates(
            roi_coordinates=self.query_params.coordinates,
            buffer_m=self.query_params.buffer,
        )

    def get_image_id(self) -> str:
        """
        Get image system id
        within date range. Selected system id
        is id of first top image sorted within date range
        based on max cloud percentage.
        Sets GEE system id of image.
        """
        roi = self.build_gee_roi()

        collection = (
            ImageCollection(self.query_params.collection)
            .filterBounds(roi)
            .filterDate(
                self.query_params.start_date.isoformat(),
                self.query_params.end_date.isoformat(),
            )
            .filter(
                Filter.lte("CLOUDY_PIXEL_PERCENTAGE", self.query_params.cloud_cover)
            )
        )

        if collection.size().getInfo() == 0:
            raise Exception("Invalid collection")

        img = collection.sort("CLOUDY_PIXEL_PERCENTAGE").first()

        return img.get("system:id").getInfo()
