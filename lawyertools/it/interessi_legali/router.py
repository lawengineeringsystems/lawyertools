from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from .main import calcola_compenso
from .data import TABELLE
from copy import deepcopy

router = APIRouter(prefix="/interessi_legali")
SERIALIZABLE_TABELLE = deepcopy(TABELLE)
SERIALIZABLE_TABELLE["tabelle"]["p2018"]["regole"]["numero_parti"][
    "aumento_max"] = "lambda x: (x - 1) * 0.3 if x <= 10 else 2.7 + (x - 10) * 0.1 if x <= 30 else 4.7"


class CompensoAvvocati(BaseModel):
    pkey: str = "p2018"
    competenza: str = "GIUDIZI ORDINARI E SOMMARI DI COGNIZIONE INNANZI AL TRIBUNALE"
    valore: int
    fasi: dict[str, int]
    cpa: bool = False
    iva: bool = False
    regole: dict = None


@router.post("/calcola/")
def _calcola_compenso(q: CompensoAvvocati):
    try:
        res = calcola_compenso(
            pkey=q.pkey,
            competenza=q.competenza,
            valore=q.valore,
            fasi=q.fasi,
            cpa=q.cpa,
            iva=q.iva,
            **q.regole
        )
        return JSONResponse(
            status_code=200,
            content=res
        )
    except Exception as e:
        return JSONResponse(status_code=422, content=dict(error=str(e)))


@router.get("/tabelle")
def _tabelle():
    return JSONResponse(status_code=200, content=SERIALIZABLE_TABELLE)
