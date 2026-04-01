from abc import ABC, abstractmethod
from src.domain.query import QueryParameters


class ImagerySource(ABC):
    """
    Abstract base class for all imaging sources. Contains search
    abstractmethod where should be part of fetching data about the
    asset from server. Fetch defines place where data should be downloaded.
    """

    @abstractmethod
    def search(self, query: QueryParameters):
        pass

    @abstractmethod
    def fetch(self, item):
        pass
