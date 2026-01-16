from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import settings
from .database import engine
from .auth import router as auth_router
from .ai import router as ai_router

app = FastAPI(title="Beginner AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
