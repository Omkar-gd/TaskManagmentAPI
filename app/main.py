from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.tasks import router as task_router

# Create FastAPI application
app = FastAPI(title="Task Management REST API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Register task router
app.include_router(task_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Task Management API is running"}
