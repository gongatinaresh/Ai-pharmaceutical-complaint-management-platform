from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models.complaint import Complaint

from app.api.complaints import router as complaints_router
from app.api.upload import router as upload_router
from app.api.ai import router as ai_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AIVOA AI Complaint Management System",
    description="AI-powered customer complaint management system",
    version="1.0.0"
)


# CORS - allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AIVOA Complaint Management API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


# API routers
app.include_router(complaints_router)
app.include_router(upload_router)
app.include_router(ai_router)