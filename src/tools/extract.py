
import traceback
from src.authorization.auth import *
from src.tools.gee_utils import S2Config, S2Downloader
from pathlib import Path
import geemap
import ee
import os

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":

    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)

    s2_config = S2Config(datadir=DATA_DIR,
                         collection='COPERNICUS/S2_SR_HARMONIZED',
                         scale=10,
                         cloud_perc=30,
                         bands=['B4', 'B3', 'B2', 'B8'],
                         roi_coordinates=[22.229681, 50.554120])

    s2_downloader = S2Downloader(s2_config)

    roi = s2_downloader.build_roi(buffer_m=350)
    img_system_id = s2_downloader.find_image_id(roi=roi,
                                                start_date='2022-04-01',
                                                end_date='2022-05-30')
    scene_metadata = s2_downloader.get_metadata_from_col_id(img_system_id)

    image_id = scene_metadata.get('image_id')
    product_id = scene_metadata.get('product_id')
    s2_downloader.export_geotiff(image_id = image_id,
                                 image_roi = roi,
                                 product_id=product_id)














    #data_to_find = {
    #    "roi_coordinates":[22.229681, 50.554120],
    #    "collection":'COPERNICUS/S2_SR_HARMONIZED',
    #    "start_date":'2023-09-01',
    #    "end_date":'2023-10-31',
    #    "cloud_percentage": 30
    #}


    #img_metadata = get_metadata(img_id)
    #print(img_metadata)
#
    ##safe_id = img_id.replace("/", "_")
    #product_id = img_metadata.get("product_id")
    #os.makedirs("data", exist_ok=True)
    #target_path = DATA_DIR / f"{product_id}.tif"
#
    #print(f'Selected image id: {img_id}')
#
    #if img_id:
    #    download_image_by_id(image_id=img_id,
    #                         output_path=str(target_path),
    #                         image_roi=roi)
    #else:
    #    print('Image with given parameters has not been found')

