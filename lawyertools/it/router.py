from fastapi import APIRouter
from .compenso_avvocati.router import router as compenso_avvocati_router
from .interessi_legali.router import router as interessi_legali_router

router = APIRouter(prefix="/it")
router.include_router(compenso_avvocati_router)
router.include_router(interessi_legali_router)
