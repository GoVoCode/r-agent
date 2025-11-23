from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router
from backend.core import get_settings, get_logger

settings = get_settings()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting server on {settings.backend_host}:{settings.backend_port}")
    yield
    logger.info("Shutting down server")


app = FastAPI(
    title="Restaurant Chat Agent API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

logger.info("FastAPI application initialized")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
        log_level=settings.log_level.lower()
    )

