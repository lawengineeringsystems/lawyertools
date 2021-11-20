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
    if cap_unit == "days":
        assert capitalizzazione >= 30, f"La capitalizzazione non può essere inferiore a un mese"
    interessi_parziali = []
    interessi_totali = 0.0
    assert (dal >= TABELLA[0][0]), f"Data minima ammessa: {TABELLA[0][0].isoformat()}"
    if capitalizzazione > 0:
        new_dal, new_al = dal, dal + relativedelta(**{cap_unit: capitalizzazione})
        new_al = min(new_al, al)
        while True:
            res = calcola_interessi(capitale, new_dal, new_al)
            capitale += res["interessi_totali"]
            interessi_totali += res["interessi_totali"]
            interessi_parziali.extend(res["interessi_parziali"])
            new_dal = new_al + relativedelta(days=1)
            new_al = new_dal + relativedelta(**{cap_unit: capitalizzazione})
            if new_dal > al:
                break
            new_al = min(new_al, al)
        return dict(interessi_totali=round(interessi_totali, 2), interessi_parziali=interessi_parziali)
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
        interessi = round(capitale * saggio * giorni_parziali / 36500, 2)
        interessi_parziali.append(dict(dal=_dal, al=_al, saggio=saggio, giorni=giorni_parziali, interessi=interessi))
        interessi_totali += interessi
    return dict(interessi_totali=round(interessi_totali, 2), interessi_parziali=interessi_parziali)


if __name__ == '__main__':
    res = calcola_interessi(1000, "1970-01-01", datetime.date.today(),
                            capitalizzazione=3, cap_unit="mesi")
    for __dal, __al, __saggio, __giorni, __interessi in res["interessi_parziali"]:
        print(
            f"dal {__dal.strftime('%d-%m-%Y')} al {__al.strftime('%d-%m-%Y')}: {__saggio}%, {__giorni} giorni, interessi: {__interessi}")
    print(res["interessi_totali"])
