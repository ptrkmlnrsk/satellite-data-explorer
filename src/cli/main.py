import argparse

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.data_access.gee.gee_service import GEEImageService
from src.data_access.gee.orchestrator import Orchestrator
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService

# from src.data_access.gee.utils.get_metadata import (
#    get_gee_metadata_of_image,
# )
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections
from src.domain.enums.bands import Bands

# TODO kompletny bajzel do ogarniecia, to powinno mieć tylko cos w stylu "run_pipeline"


def main():
    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)
    print("Earth Engine initialized successfully!")

    # bands = Bands

    parser = argparse.ArgumentParser(description="Satellite data downloader")

    parser.add_argument(
        "--dataset", type=str, help="Available datasets: ", required=True
    )
    parser.add_argument(
        "--roi", type=str, help="Coordinates of the ROI in format lat,lon"
    )
    parser.add_argument(
        "--collection",
        type=str,
        choices=[d.value for d in Collections],
        help="Available collections",
        required=True,
    )
    parser.add_argument("--start_date", type=str, help="Date in format YYYY-MM-DD")
    parser.add_argument("--end_date", type=str, help="Date in format YYYY-MM-DD")
    parser.add_argument("--cloud_cover", type=int, help="Cloud cover percentage")
    parser.add_argument(
        "--bands",
        type=str,
        nargs="+",
        choices=[b.value for b in Bands],
        help="Available bands: ",
    )

    args = parser.parse_args()

    collection_enum = Collections(args.collection)
    bands_enum = [Bands(b) for b in args.bands] if args.bands else []

    query_parameters = QueryParameters(
        dataset=args.dataset,
        collection=collection_enum,
        start_date=args.start_date,
        end_date=args.end_date,
        coordinates=args.roi,
        cloud_cover=args.cloud_cover,
        bands=bands_enum,
    )

    gee_image_info_service = GEEImageInfoService(query_parameters)
    gee_image_downloader = GEEImageDownloader()

    gee_service = GEEImageService(
        query_parameters, gee_image_info_service, gee_image_downloader
    )
    orchestrator = Orchestrator()
    orchestrator.set_source(gee_service)
    orchestrator.run_process()
