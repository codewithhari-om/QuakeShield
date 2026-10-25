
from fastapi import FastAPI
import uvicorn

app = FastAPI()

latest_event = {
    "alert": False,
    "message": "No test alert"
}

@app.get("/health")
def health():
    return {"status": "online"}

@app.get("/test-alert")
def test_alert():
    global latest_event
    latest_event = {
        "alert": True,
        "message": "QuakeShield test alert. This is a simulation, not a confirmed earthquake."
    }
    return latest_event

@app.get("/latest-event")
def get_latest_event():
    return latest_event

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
