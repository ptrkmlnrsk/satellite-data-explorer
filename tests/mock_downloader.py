from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.tools.gee_utils import get_bounds_from_coordinates
from pathlib import Path
from src.config import SentinelConfig
from src.pipeline.exporter_pipeline import Exporter
from src.pipeline.downloader_pipeline import SentinelDownloader

CURRENT_FILE = Path(__file__).resolve()  # pelna sciezka pliku w ktorym jestm
PROJECT_ROOT = CURRENT_FILE.parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Google Auth
    credentials = authenticate_google_api()
    # Engine init
    initialize_earth_engine(credentials)

    # some configs
    s2_config = SentinelConfig(
        collection="COPERNICUS/S2_SR_HARMONIZED",
        bands=["B4", "B3", "B2", "B8"],
        roi_coordinates=[22.229681, 50.554120],
    )

    roi = get_bounds_from_coordinates(
        buffer_m=350, roi_coordinates=s2_config.roi_coordinates
    )

    s2_downloader = SentinelDownloader(s2_config.collection)
    s2_downloader.set_system_id(roi=roi, start_date="2022-04-01", end_date="2022-05-30")
    scene_metadata = s2_downloader.get_metadata_for_image()

    image_id = scene_metadata.get("image_id")

    product_id = scene_metadata.get("product_id")

    exporter = Exporter(s2_config.bands)
    exporter.export_geotiff(image_id=image_id, image_roi=roi, product_id=product_id)
