import datetime
from dateutil.relativedelta import relativedelta

from .data import TABELLA

# I = C * s * t / 36500


CAP_UNIT_MAP = dict(giorni="days", mesi="months", anni="years")
ALLOWED_CAP_UNITS = set(list(CAP_UNIT_MAP.keys()) + list(CAP_UNIT_MAP.values()))


def calcola_interessi(
        capitale: float,
        dal: (datetime.date, str),
        al: (datetime.date, str),
        capitalizzazione: int = 0,
        cap_unit: str = "months"
):
    if isinstance(dal, str):
        dal = datetime.datetime.strptime(dal, "%Y-%m-%d").date()
    if isinstance(al, str):
        al = datetime.datetime.strptime(al, "%Y-%m-%d").date()
    cap_unit = CAP_UNIT_MAP.get(cap_unit, cap_unit)
    assert cap_unit in ALLOWED_CAP_UNITS, f"Unità di capitalizzazione non valida: {cap_unit}." \
                                          f"Unità ammesse: {ALLOWED_CAP_UNITS}"
    interessi_parziali = []
    interessi_totali = 0.0
    assert (dal >= TABELLA[0][0]), f"Data minima ammessa: {TABELLA[0][0].strftime('%Y-%m-%d')}"
    if capitalizzazione > 0:
        new_dal, new_al = dal, dal + relativedelta(**{cap_unit: capitalizzazione})
        new_al = min(new_al, al)
        while True:
            _it, _ip = calcola_interessi(capitale, new_dal, new_al)
            capitale += _it
            interessi_totali += _it
            interessi_parziali.extend(_ip)
            new_dal = new_al + relativedelta(days=1)
            new_al = new_dal + relativedelta(**{cap_unit: capitalizzazione})
            if new_dal > al:
                break
            new_al = min(new_al, al)
        return interessi_totali, interessi_parziali
    for _dal, _al, saggio in TABELLA:
        _al = _al or al
        _al = min(_al, al)
        if al < _dal:
            break
        if dal > _al:
            continue
        _dal = max(_dal, dal)
        td = _al - _dal
        giorni_parziali = td.days
        interessi = capitale * saggio * giorni_parziali / 36500
        interessi_parziali.append((_dal, _al, saggio, giorni_parziali, interessi))
        interessi_totali += interessi
    return dict(interessi_totali=interessi_totali, interessi_parziali=interessi_parziali)


if __name__ == '__main__':
    _interessi_totali, _interessi_parziali = calcola_interessi(1000, "1970-01-01", datetime.date.today(),
                                                               capitalizzazione=3, cap_unit="mesi")
    for __dal, __al, __saggio, __giorni, __interessi in _interessi_parziali:
        print(
            f"dal {__dal.strftime('%d-%m-%Y')} al {__al.strftime('%d-%m-%Y')}: {__saggio}%, {__giorni} giorni, interessi: {__interessi}")
    print(_interessi_totali)
