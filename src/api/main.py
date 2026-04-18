from fastapi import FastAPI
from pydantic import BaseModel

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.data_access.gee.gee_service import GEEImageService
from src.data_access.gee.orchestrator import Orchestrator
from src.data_access.gee.image_downloader import GEEImageDownloader
from src.data_access.gee.image_info_service import GEEImageInfoService
from src.domain.query import QueryParameters
from src.domain.enums.collections import Collections

app = FastAPI()


class RunRequest(BaseModel):
    dataset: str
    coordinates: list[float] | None = None
    collection: Collections
    start_date: str | None = None
    end_date: str | None = None
    cloud_cover: int | None = None
    bands: list[str] = ["B2", "B3", "B4"]


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)


@app.post("/run")
def run_pipeline(payload: RunRequest):
    collection_enum = Collections(payload.collection)

    query_parameters = QueryParameters(
        dataset=payload.dataset,
        collection=collection_enum,
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
    orchestrator.run_process()

    return {
        "message": "Pipeline executed",
        "collection": payload.collection,
        "dataset": payload.dataset,
        "bands": payload.bands,
    }
