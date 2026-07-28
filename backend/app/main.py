import sys
import io
import logging

# Ensure stdout supports Unicode on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

from fastapi import FastAPI
import asyncio
import logging
from contextlib import asynccontextmanager

from app.database.connection import connect_to_mongodb, close_mongodb_connection
from app.middleware.cors import add_cors
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.schemes import router as schemes_router
from app.routes.recommendations import router as recommendations_router
from app.routes.ai import router as ai_router
from app.routes.admin import router as admin_router
from app.routes.notifications import router as notifications_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    # Warm up embedding model in background so first request isn't slow
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _warmup_embedding)
    yield
    await close_mongodb_connection()


def _warmup_embedding():
    try:
        from app.agents.embedding_model import get_embedding_model
        get_embedding_model()
        logger.info("Embedding model warmed up")
    except Exception as e:
        logger.warning(f"Embedding model warmup failed: {e}")


app = FastAPI(
    title="NeuraScheme AI API",
    version="1.0.0",
    lifespan=lifespan,
)

add_cors(app)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(schemes_router)
app.include_router(recommendations_router)
app.include_router(ai_router)
app.include_router(admin_router)
app.include_router(notifications_router)


@app.get("/")
async def root():
    return {"message": "Welcome to NeuraScheme AI 🚀"}
