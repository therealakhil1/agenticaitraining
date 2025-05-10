import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Interview Agent API")
@app.get("/")
async def root():
    return {'hello':'world from akhil'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)