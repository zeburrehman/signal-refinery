from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import filings, financials, health
from database import engine, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Signal Refinery API",
    description="Financial signal analysis API",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure more restrictively in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(filings.router)
app.include_router(financials.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring"""
    return {"status": "healthy"}

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
