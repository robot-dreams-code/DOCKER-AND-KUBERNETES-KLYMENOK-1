from fastapi import FastAPI
from .routers.health import router as health_router
from .routers.v1.items import router as items_router
from .config import settings

app = FastAPI(
    title="My Lesson 3 Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health_router, prefix="")
app.include_router(items_router, prefix="/v1")

@app.get("/")
def root():
    return {
        "service": "lesson3",
        "env": settings.APP_ENV,
        "message": "Lesson3 on port 8080 is running!"
    }
