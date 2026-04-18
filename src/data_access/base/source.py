from abc import ABC, abstractmethod

from src.domain.image_request import ImageRequest
from src.domain.metadata import ImageMetadata


class ImagerySource(ABC):
    """
    Abstract base class for all imaging sources. Contains search
    abstractmethod where should be part of fetching data about the
    asset from server. Fetch defines place where data should be downloaded.
    """

    @abstractmethod
    def search(self) -> str:
        pass

    @abstractmethod
    def get_metadata(self, image_id: str) -> ImageMetadata:
        pass

    @abstractmethod
    def download(self, image_request: ImageRequest):  # raster?
        pass

    # TODO porownywarki
    # @abstractmethod
    # def compare(self): # com
    # wyjście z search jest takie samo, niezaleznie od źródła danych
    # aby umozliwić porównanie
    #    pass
