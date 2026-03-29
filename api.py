from fastapi import FastAPI

app = FastAPI()
controller = None   # injected at startup

@app.get("/status")
def status():
    return [
        {
            "caption": box.caption,
            "payload": box.payload,
            "doseRate": box.doseRate,
            "remaining": box.remainingSeconds,
            "colour": box.displayColour,
            "endTime": box.end_time,
        }
        for box in controller._boxes.items
    ]