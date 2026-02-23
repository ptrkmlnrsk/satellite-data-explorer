from src.db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid


class Metadata(Base):
    __tablename__ = "metadata"
    __table_args__ = {"schema": "catalog"}

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    image_id: Mapped[str]
    product_id: Mapped[str]
    acquired_at: Mapped[datetime.datetime]
    cloud_percent: Mapped[float]
    mgrs_tile: Mapped[str]
    platform: Mapped[str]
    processing_baseline: Mapped[str]
    processing_level: Mapped[str]
    product_type: Mapped[str]
