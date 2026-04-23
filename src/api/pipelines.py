from src.data_access.gee.gee_service import GEEImageService
from src.data_access.gee.orchestrator import Orchestrator
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections
from src.api.schemas.run_request import Sentinel2Request

from fastapi import APIRouter

router = APIRouter()


# wszystko co poniżej to przerzucic do innego pliku
# zrobic sobie router
@router.post("/run")
def run_pipeline(payload: Sentinel2Request):
    print(payload)
    print(payload.bands[0].is_10m)
    collection_enum = Collections(payload.collection)

    query_parameters = QueryParameters(
        dataset=payload.dataset,
        coordinates=payload.coordinates,
        collection=collection_enum.SENTINEL_2.value,
        start_date=payload.start_date,
        end_date=payload.end_date,
        cloud_cover=payload.cloud_cover,
        bands=payload.bands,
    )

    gee_image_info_service = GEEImageInfoService(query_parameters)
    gee_image_downloader = GEEImageDownloader()
    gee_service = GEEImageService(
        query_parameters,
        gee_image_info_service,
        gee_image_downloader,
    )

    orchestrator = Orchestrator()
    orchestrator.set_source(gee_service)
    result = orchestrator.run_process()

    # return {
    #    "message": "Pipeline executed",
    #    "collection": payload.collection,
    #    "dataset": payload.dataset,
    #    "bands": payload.bands,
    # }
    return result
