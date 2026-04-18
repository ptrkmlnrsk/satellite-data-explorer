from dataclasses import dataclass


@dataclass
class ImageMetadata:
    image_id: str
    product_id: str
    acquired_at: str
    cloud_pct: float
    mgrs_tile: str
    platform: str
    processing_baseline: str
    processing_level: str
    product_type: str
