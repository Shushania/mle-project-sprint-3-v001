
import os
import psutil
from fastapi import FastAPI
from random import randint, uniform
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Gauge
from dotenv import load_dotenv

from .fast_api_handler import FastApiHandler

load_dotenv()
feature_flag = os.getenv('FLAG', 'False').lower() == 'true'

app = FastAPI()
app.handler = FastApiHandler()
if feature_flag:
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)
    
    price_predictions = Histogram(
    "price_predictions",
    "Histogram of predictions",
    buckets=list(range((10**6), 1*(10**8) + 5*(10**6), 5*(10**6)))
    )
    CPU_USAGE = Gauge('custom_cpu_usage_percent', 'CPU usage percent')
    DISK_USAGE = Gauge('custom_disk_usage_percent', 'Disk usage percent')
    MEMORY_USAGE = Gauge('custom_memory_usage_percent', 'Memory usage percent')



@app.get("/service-status")
def health_check():
    return {"status": "ok"}


@app.post("/predict") 
def get_prediction(model_params: dict):
    price = app.handler.handle(model_params)
    if feature_flag:
        price_predictions.observe(price['score'])
        CPU_USAGE.set(psutil.cpu_percent(interval=1))
        DISK_USAGE.set(psutil.disk_usage('/').percent)
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return price

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
    price = app.handler.handle(random_params)
    if feature_flag:
        price_predictions.observe(price['score'])
        CPU_USAGE.set(psutil.cpu_percent(interval=1))
        DISK_USAGE.set(psutil.disk_usage('/').percent)
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return (random_params, price)