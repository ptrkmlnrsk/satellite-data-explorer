from ee import ImageCollection, Filter
from src.domain.query import QueryParameters


class GEEImageInfoService:
    """
    Gets parameters from QueryParameters object and returns asset system id
    and metadata
    """

    def __init__(self, query_params: QueryParameters):
        self.query_params = query_params

    def get_image_id(self) -> None:
        """
        Get image system id
        within date range. Selected system id
        is id of first top image sorted within date range
        based on max cloud percentage.
        Sets GEE system id of image.
        """

        collection = (
            ImageCollection(self.query_params.collection)
            .filterBounds(self.query_params.roi)
            .filterDate(self.query_params.start_date, self.query_params.end_date)
            .filter(
                Filter.lte("CLOUDY_PIXEL_PERCENTAGE", self.query_params.cloud_cover)
            )
        )

        if collection.size().getInfo() == 0:
            raise Exception("Invalid collection")

        img = collection.sort("CLOUDY_PIXEL_PERCENTAGE").first()

        return img.get("system:id").getInfo()
