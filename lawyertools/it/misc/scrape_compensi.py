from bs4 import BeautifulSoup
import re
import json


def get_header(element):
    def is_header(_t):
        if a := _t.find("a"):
            name = a.attrs.get("name")
            if name is not None:
                return re.match(r"par\d+", name)
        return False
    target = element
    while not is_header(target):
        target = target.find_previous_sibling()
    raw_text = target.text
    _h = re.sub(r"^\d+\.", r"", raw_text.strip())
    return _h.strip()


def get_value(td):
    raw_text = td.text
    try:
        nt = raw_text.split()[-1]
    except Exception:
        print(raw_text)
        raise
    nt = re.sub(r",\d+", "", nt)
    nt = nt.replace(".", "")
    return int(nt)


soup = BeautifulSoup(open("tabelle.html"), "html.parser")
tables = soup.find_all("table")

TABLES = dict()
TABLES["tabelle"] = dict(p2018=dict(competenza=dict()))

for table in tables:
    header = get_header(table)
    if header == "GIUDIZI PENALI":
        continue
    rows = table.find_all("tr")
    row_valore = rows[0]

    tds_valore = row_valore.find_all("td")
    data = dict()
    data["scaglioni"] = [get_value(td) for td in tds_valore[1:]]
    data["fasi"] = dict()
    for row in rows[1:]:
        tds_fase = [td for td in row.find_all("td") if str(td.text).strip() != ""]
        if len(tds_fase) > 0:
            key = re.sub(r"^\d+\.", r"", tds_fase[0].text.strip()).strip()
            data["fasi"][key] = [get_value(td) for td in tds_fase[1:]]
    TABLES["tabelle"]["p2018"]["competenza"][header] = data

with open("compensi_avvocati.json", "w") as f:
    json.dump(TABLES, f, indent=4)

