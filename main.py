from fastapi import FastAPI
from routes.sensor import router as sensor_router
from mqtt_client import start_mqtt

app = FastAPI(title="AquaLeak API")
app.include_router(sensor_router, prefix="/api")

@app.on_event("startup")
async def startup():
    try:
        start_mqtt()
    except Exception as e:
        print(f"MQTT skipped: {e}")

@app.get("/")
def root():
    return {"status": "AquaLeak backend running"}