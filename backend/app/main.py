import sys
import io

# Ensure stdout supports Unicode on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.connection import connect_to_mongodb, close_mongodb_connection
from app.middleware.cors import add_cors
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.schemes import router as schemes_router
from app.routes.recommendations import router as recommendations_router
from app.routes.ai import router as ai_router
from app.routes.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


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


@app.get("/")
async def root():
    return {"message": "Welcome to NeuraScheme AI 🚀"}
