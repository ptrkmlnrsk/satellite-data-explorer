from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.data_access.gee.gee_service import GEEImageService
from src.data_access.gee.orchestrator import Orchestrator
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections
from src.api.schemas.run_request import RunRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)

    print("Earth Engine initialized successfully!")

    yield

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/run")
def run_pipeline(payload: RunRequest):
    collection_enum = Collections(payload.collection)

    query_parameters = QueryParameters(
        dataset=payload.dataset,
        collection=collection_enum.SENTINEL_2.value,
        start_date=payload.start_date,
        end_date=payload.end_date,
        coordinates=payload.coordinates,
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
