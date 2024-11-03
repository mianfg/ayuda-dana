import uvicorn
from ayuda_dana_backend.routers.v1 import router as v1
from fastapi import FastAPI, status
from fastapi.responses import Response
from mongoengine import connect

# WIP store secrets
connect(
    host="",
    db="ayuda-dana",
)

app = FastAPI(
    title="ayuda-dana-backend",
    description="Backend for ayuda-dana",
    version="0.1.0",
    contact={
        "name": "mianfg",
        "url": "https://mianfg.me",
        "email": "hello@mianfg.me",
    },
)

app.include_router(v1, prefix="/v1")


@app.get("/health-check")
async def health_check():
    """Check health"""
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True, workers=3)
