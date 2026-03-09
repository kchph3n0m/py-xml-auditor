import fastapi
from app.api.routes import router

app = fastapi.FastAPI(title="XML Auditor Microservice", version="1.0.0")

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Simple endpoint to verify the service is running."""
    return {"status": "ok"}