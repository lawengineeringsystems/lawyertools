from fastapi import APIRouter
from .compenso_avvocati.router import router as compenso_avvocati_router


router = APIRouter(prefix="/it")
router.include_router(compenso_avvocati_router)
