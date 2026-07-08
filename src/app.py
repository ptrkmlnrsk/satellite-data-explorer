from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.api.pipelines import router as pipeline_router
from src.logging_config import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("INFO")

    credentials = authenticate_google_api()
    logger.info("Authentication to Google Earth engine complete.")

    initialize_earth_engine(credentials)

    logger.info("Earth Engine initialized successfully!")

    yield

    logger.info("Shutting down.")


app = FastAPI(lifespan=lifespan)

app.include_router(pipeline_router)


@app.get("/")
def healthcheck():
    logger.info("Healthcheck called")
    return {"status": "ok"}
