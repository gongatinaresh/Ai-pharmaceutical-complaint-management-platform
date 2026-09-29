from fastapi import FastAPI

app = FastAPI(
    title="AIVOA AI Complaint Management System",
    description="AI-powered customer complaint management system for pharmaceutical manufacturing",
    version="1.0.0"
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