from fastapi import APIRouter, HTTPException
import logging

from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService
from src.data_access.gee.utils.get_metadata import get_gee_metadata_of_image
from src.data_access.gee.utils.get_image_preview import get_image_preview
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections
from src.domain.image_request import GEEImageRequest
from src.api.schemas.run_request import Sentinel2Request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/search")
def search_image(request: Sentinel2Request):
    logger.info("Search image requested")
    # Pydantic model -> co zwraca endpoint
    collection_enum = Collections(request.collection)

    logger.info("Found collection")

    query_parameters = QueryParameters(  # dataclass -> input usera
        dataset=request.dataset,
        coordinates=request.coordinates,
        collection=collection_enum.value,
        start_date=request.start_date,
        end_date=request.end_date,
        cloud_cover=request.cloud_cover,
        bands=request.bands,
    )
    gee_image_info_service = GEEImageInfoService(query_parameters)
    image_id = gee_image_info_service.get_image_id()

    metadata = get_gee_metadata_of_image(image_id)

    logger.info("Downloaded metadata")

    return metadata


@router.post("/preview")
def preview_image(request: GEEImageRequest):
    try:
        url = get_image_preview(request)
        return {"preview_url": url}
    except Exception:
        logger.exception(
            "Failed to obtain image preview. image_id=%s", request.image_id
        )
        raise HTTPException(
            status_code=500, detail="Failed to obtain image preview."
        ) from exec


@router.post("/download")
def download_image(request: GEEImageRequest):
    try:
        logger.info("Download requested. image_id=%s", request.image_id)
        gee_image_downloader = GEEImageDownloader()
        gee_image_downloader.export_geotiff(request)
        logger.info("Downloaded image. image_id=%s", request.image_id)

    except Exception:
        logger.exception("Failed to download image. image_id=%s", request.image_id)
        raise HTTPException(
            status_code=500,
            detail="Failed to download image",
        ) from exec
