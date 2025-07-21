from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core import get_settings
from app.api.routers import router
from app.message_broker import RabbitMQ
from app.api.schemas import PublishMessageRequest
import uvicorn
import os
import json

import logging
logging.basicConfig(level=logging.INFO)

settings = get_settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit_mq = RabbitMQ(settings.RABBITMQ_CONNECTION_URL)
    await rabbit_mq.connect()
    app.state.rabbit_mq_send = rabbit_mq.send_message
    yield
    await rabbit_mq.close()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.post("/publisher/publish")
async def publish_message(payload: PublishMessageRequest):
    if not hasattr(app.state, 'rabbit_mq_send'):
        raise RuntimeError("RabbitMQ connection is not established.")
    await app.state.rabbit_mq_send(json.dumps(payload.model_dump(exclude_none=True)))
    return {"message": "Message sent to RabbitMQ"}

# print all settings
for key, value in settings.model_dump().items():
    pass
    # print(f"{key}: {value}")

app.include_router(router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.APP_MODE == "DEVELOPMENT",
    )