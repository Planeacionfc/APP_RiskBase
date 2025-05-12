from fastapi import APIRouter
from .auth import router as auth_router
from .risk_process import router as risk_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(risk_router)
