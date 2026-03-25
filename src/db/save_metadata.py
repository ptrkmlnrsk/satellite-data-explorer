from src.models.metadata import Metadata
from src.db.session import Session


def upload_metadata_to_db(scene_metadata: dict[str, str | int]):
    with Session() as session:
        obj = Metadata(**scene_metadata)
        session.add(obj)
        session.commit()
