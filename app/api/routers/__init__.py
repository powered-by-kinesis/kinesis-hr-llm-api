from fastapi import APIRouter
from .conversations import router as conversations_router
from .stores import router as stores_router
from .webhook import router as webhook_router

router = APIRouter()
router.include_router(conversations_router)
router.include_router(stores_router)
router.include_router(webhook_router)
