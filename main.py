from fastapi import FastAPI
from app.core import get_settings
from app.api.routers import router
import uvicorn
import os

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)


os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# print all settings
for key, value in settings.model_dump().items():
    print(f"{key}: {value}")

app.include_router(router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )