import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Interview Agent API")
@app.get("/")
async def root():
    return {'hello':'world from akhil on 10th may'}

@app.get("/healthz", tags=["health"])
async def healthz():
    """
    Simple liveness/readiness check.
    Returns HTTP 200 if the app is up.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)