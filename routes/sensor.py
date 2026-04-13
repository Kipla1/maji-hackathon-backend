import csv
import os
from fastapi import APIRouter

router = APIRouter()
DATA_FILE = "data/readings.csv"

@router.get("/readings")
def get_readings():
    if not os.path.isfile(DATA_FILE):
        return {"data": [], "message": "No readings yet"}
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        readings = list(reader)
    return {"data": readings}

@router.get("/status")
def get_status():
    return {"broker": "broker.hivemq.com", "topic": "maji/sensors/vibration", "status": "listening"}

# @router.post("/readings")
# def post_readings:
#     return