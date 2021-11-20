import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from .data import TABELLA
from .main import calcola_interessi
from ...utils import DatetimeEncoder

router = APIRouter(prefix="/interessi_legali")


class InteressiLegali(BaseModel):
    capitale: float
    dal: str
    al: str
    capitalizzazione: int = 0
    cap_unit: str = "mesi"


@router.post("/calcola_interessi/")
def _calcola_compenso(q: InteressiLegali):
    try:
        res = calcola_interessi(
            capitale=q.capitale,
            dal=q.dal,
            al=q.al,
            capitalizzazione=q.capitalizzazione,
            cap_unit=q.cap_unit
        )
        return Response(
            status_code=200,
            content=json.dumps(res, cls=DatetimeEncoder),
            media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(status_code=422, content=dict(error=str(e)))


@router.get("/tabella")
def _tabelle():
    tabella = json.dumps(TABELLA, cls=DatetimeEncoder)
    return Response(status_code=200, content=tabella, media_type="application/json")
