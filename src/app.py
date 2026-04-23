from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.authorization.auth import authenticate_google_api, initialize_earth_engine
from src.api.pipelines import router as pipeline_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    credentials = authenticate_google_api()
    initialize_earth_engine(credentials)

    print("Earth Engine initialized successfully!")

    yield

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(pipeline_router)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
