'''
napisz mi narzedzie ktore zrobi predykcje czegos i jakie bedzie PPM
'''

from fastapi import FastAPI
from pydantic import BaseModel
import src.tools.gee_utils as gee

app = FastAPI()

class Location(BaseModel):
    lat: float
    lon: float
    start_date: str
    end_date: str

@app.post("/predict_pm25")
def predict_pm25(location: Location):
    pm25_value = gee.get_pm25(location.lat, location.lon,
                              location.start_date, location.end_date)
    return {"pm25_value": pm25_value}
