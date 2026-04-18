from pydantic import BaseModel
from src.domain.enums.collections import Collections


class RunRequest(BaseModel):
    dataset: str
    coordinates: list[float] | None = None
    collection: Collections
    start_date: str | None = None
    end_date: str | None = None
    cloud_cover: int | None = None
    bands: list[str] = ["B2", "B3", "B4"]
