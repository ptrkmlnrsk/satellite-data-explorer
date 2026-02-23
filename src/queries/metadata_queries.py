from src.db.models.metadata import Metadata
from src.db.session import Session


def upload_metadata_to_db(metadata: dict[str, str]):
    metadata_obj = Metadata(
        image_id=metadata["image_id"],
        product_id=metadata["product_id"],
        acquired_at=metadata["acquired_at"],
        cloud_percent=metadata["cloud_percent"],
        mgrs_tile=metadata["mgrs_tile"],
        platform=metadata["platform"],
        processing_baseline=metadata["processing_baseline"],
        processing_level=metadata["processing_level"],
        product_type=metadata["product_type"],
    )
    with Session() as session:
        session.add(metadata_obj)
        session.commit()
