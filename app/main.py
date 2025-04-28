# This is our main.py 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api import api_router  
from app.config import settings
from app.database.db import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Library Management System API",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


# Create tables at startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Dr. B.S. Library Management System API",
        "documentation": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}