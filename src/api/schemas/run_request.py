from pydantic import BaseModel, field_validator
from src.domain.enums.collections import Collections
from datetime import date

from src.domain.enums.sentinel2_bands import Sentinel2Band


class Sentinel2Request(BaseModel):
    """Pydantic model for the request body"""

    dataset: str
    coordinates: list[float] | None = None
    collection: Collections
    start_date: date | None = None
    end_date: date | None = None
    cloud_cover: int | None = None
    bands: list[Sentinel2Band]

    # zanim sie stworzy obiekt tej klasy to zostanie wywolany ten walidator
    @field_validator("bands", mode="before")
    def parse_bands(
        cls, bands
    ):  # to jakie pole podam w walidatorze to jego wartosc bedzie pod bands
        return [Sentinel2Band.from_any(b) for b in bands]
