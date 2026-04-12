import argparse

from src.data_access.gee.gee_service import GEEImageService
from src.data_access.gee.orchestrator import Orchestrator
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService

# from src.data_access.gee.utils.get_metadata import (
#    get_gee_metadata_of_image,
# )
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections


def main():
    collections = Collections
    parser = argparse.ArgumentParser(description="Satellite data downloader")

    parser.add_argument(
        "--dataset", type=str, help="Available datasets: ", required=True
    )
    parser.add_argument(
        "--collections",
        type=str,
        help="Available collections: " + str([d.value for d in collections]),
        required=True,
    )
    parser.add_argument("--start_date", type=str, help="Date in format YYYY-MM-DD")
    parser.add_argument("--end_date", type=str, help="Date in format YYYY-MM-DD")
    parser.add_argument(
        "--roi", type=str, help="Coordinates of the ROI in format lat,lon"
    )

    collections = Collections
    query_parameters = QueryParameters()
    gee_image_info_service = GEEImageInfoService(query_parameters)
    gee_image_downloader = GEEImageDownloader()

    gee_service = GEEImageService(
        query_parameters, gee_image_info_service, gee_image_downloader
    )
    orchestrator = Orchestrator()
    orchestrator.set_source(gee_service)
    orchestrator.run_process()
