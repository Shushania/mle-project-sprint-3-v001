
from fastapi import FastAPI
from random import randint, uniform

from .fast_api_handler import FastApiHandler


app = FastAPI()
app.handler = FastApiHandler()

@app.get("/service-status")
def health_check():
    return {"status": "ok"}


@app.post("/predict") 
def get_prediction(model_params: dict):
    return app.handler.handle(model_params)

@app.get("/test")
def get_test():
    random_params = {
        "floor": randint(1, 60), 
        "is_apartment": randint(0, 1), 
        "kitchen_area": uniform(1, 100), 
        "living_area": uniform(1, 200), 
        "rooms": randint(1, 10), 
        "total_area": uniform(1, 300), 
        "building_id": randint(1, 20000), 
        "build_year": randint(1920, 2024),  
        "building_type_int": randint(1, 10), 
        "latitude": uniform(54, 56), 
        "longitude": uniform(36, 38), 
        "ceiling_height": uniform(1, 5), 
        "flats_count": randint(1, 1000), 
        "floors_total": randint(1, 60), 
        "has_elevator": randint(0, 1)
    }

    return (random_params, app.handler.handle(random_params))