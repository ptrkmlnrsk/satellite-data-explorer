from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Metadata(Base):
    __tablename__ = "metadata"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    image_id: Mapped[str]
    acquired_at: Mapped[datetime]
    cloud_percent: Mapped[int]
    mgrs_tile: Mapped[int]
    platform: Mapped[str]
    processing_baseline: Mapped[int]
    processing_level: Mapped[int]
    product_type: Mapped[str]
