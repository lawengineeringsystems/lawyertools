import math

from .data import TABELLE


SPESE_GENERALI = 0.15
IVA = 0.22
CPA = 0.04


def validate(pkey, **regole):
    params = TABELLE["tabelle"][pkey]["regole"]
    param_keys = set(params.keys())
    for key, value in regole.items():
        if key not in param_keys:
            raise KeyError(f"{key} non è un parametro valido")
        aumento_max = params[key]["aumento_max"]
        if key == "numero_parti":
            numero_parti, aumento = value
            if aumento < 0:
                raise ValueError("L'aumento non può essere negativo")
            if aumento > aumento_max(numero_parti):
                raise ValueError(
                    f"L'aumento del {aumento * 100} % è superiore al massimo consentito ({aumento_max(numero_parti)} %)"
                )
        else:
            if value < 0:
                raise ValueError("L'aumento non può essere negativo")
            if value > aumento_max:
                raise ValueError(
                    f"L'aumento del {value * 100} % è superiore al massimo consentito ({aumento_max} %)"
                )
    return params


def calcola_compenso(pkey, competenza, valore, fasi, cpa=False, iva=False, **regole):
    params = validate(pkey, **regole)
    tabella = TABELLE["tabelle"][pkey]
    tabella_competenza = tabella["competenza"][competenza]
    scaglioni = tabella_competenza["scaglioni"]
    oltre_520k = False
    for i, scaglione in enumerate(scaglioni):
        if valore <= scaglione:
            break
    else:
        if competenza == "GIUDICE DI PACE":
            raise ValueError("Il valore della controversia supera la tabella_competenza del Giudice di Pace")
        else:
            oltre_520k = True
    output = dict()

    compenso_tabellare = dict()
    output["compenso_tabellare"] = compenso_tabellare
    t0 = 0
    for fase, aumento_diminuzione in fasi.items():
        compenso_base = tabella_competenza["fasi"][fase][i]
        if oltre_520k:
            loops = math.floor(math.log(valore / 1e6) / math.log(2) + 2)
            for _ in range(loops):
                compenso_base += compenso_base * 0.3
        _t = compenso_base + compenso_base * aumento_diminuzione
        compenso_tabellare[fase] = dict(
            base=compenso_base,
            perc=aumento_diminuzione,
            totale=round(_t, 2)
        )
        t0 += _t
    compenso_tabellare["totale"] = round(t0, 2)

    t1 = 0
    aumenti = dict()
    output["aumenti"] = aumenti
    aumenti_speciali = {k: v for k, v in regole.items() if params[k]["su"] != "totale"}
    for k, v in aumenti_speciali.items():
        compenso_fase_base_key = compenso_tabellare[params[k]["su"]]
        compenso_fase_base = compenso_tabellare[compenso_fase_base_key]
        _t = compenso_fase_base["totale"] * v
        aumenti[k] = dict(
            desc=params[k]["desc"],
            su=params[k]["su"],
            perc=v,
            totale=round(_t, 2)
        )
        t1 += _t
        regole.pop(k)

    for k, v in regole.items():
        if hasattr(v, "__iter__"):
            v = v[-1]
        _t = t0 * v  # todo: check if increases are to be compounded
        aumenti[k] = dict(
            desc=params[k]["desc"],
            # su=params[k]["su"],
            perc=v,
            totale=round(_t, 2)
        )
        t1 += _t
    aumenti["totale"] = round(t1, 2)

    t2 = (t0 + t1) * SPESE_GENERALI
    accessori = dict()
    output["accessori"] = accessori
    accessori["spese_generali"] = dict(
        desc="Spese generali",
        perc=SPESE_GENERALI,
        totale=round(t2, 2)
    )

    if cpa:
        _t = (t0 + t1 + t2) * CPA
        accessori["cpa"] = dict(
            desc="CPA",
            perc=CPA,
            totale=round(_t, 2)
        )
        t2 += _t

    if iva:
        _t = (t0 + t1 + t2) * IVA
        accessori["iva"] = dict(
            desc="IVA",
            perc=IVA,
            totale=round(_t, 2)
        )
        t2 += _t

    accessori["totale"] = round(t2, 2)
    output["totale"] = round(t0 + t1 + t2, 2)

    return output


if __name__ == '__main__':
    res = calcola_compenso(
        "p2018",
        "GIUDIZI ORDINARI E SOMMARI DI COGNIZIONE INNANZI AL TRIBUNALE",
        100_000,
        {
            "Fase di studio della controversia": 0,
            "Fase introduttiva del giudizio": 0,
            "Fase istruttoria e/o di trattazione": 0,
            "Fase decisionale": 0
        },
        cpa=True,
        iva=True,
        numero_parti=(10, 2),
    )
    import json
    print(json.dumps(res, indent=4))
