import sqlite3
from pathlib import Path
import xml.etree.ElementTree as ET
import models
import mapping
from datetime import datetime


DB_PATH = Path("data/energy_data.db")

root = ET.parse("data/raw/IT_20260818_153559.xml").getroot()
NS = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}

def get_text(element, path: str, ns: dict) -> str:
    found = element.find(path, ns)
    if found is None or found.text is None:
        raise ValueError(f"Campo mancante nell'XML: {path}")
    return found.text

energy_data = []
for timeseries in root.findall("ns:TimeSeries", NS):
    fonte_el = timeseries.find("ns:MktPSRType/ns:psrType", NS)
    zona_el = timeseries.find("ns:outBiddingZone_Domain.mRID", NS)
    business_type = get_text(timeseries, "ns:businessType", NS)

    if zona_el is None:
        zona_el = timeseries.find("ns:inBiddingZone_Domain.mRID", NS)
    if zona_el is None or fonte_el is None or fonte_el.text is None or zona_el.text is None:
        raise ValueError("TimeSeries senza fonte o zona valida")

    for period in timeseries.findall("ns:Period", NS):
        data =  datetime.strptime(get_text(period, "ns:timeInterval/ns:start", NS), "%Y-%m-%dT%H:%MZ")
        for point in period.findall("ns:Point", NS):  
            position = get_text(point, "ns:position", NS)
            quantity = get_text(point, "ns:quantity", NS)
            energy_data.append(
                models.Rilevazione(zona_el.text, data, fonte_el.text, float(quantity), business_type))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(Path("schema.sql").read_text())
    return conn

conn = get_connection()

def inserisci_db(energy_data: list, conn) -> int:
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO rilevazioni (paese, data, fonte, valore_mw, tipo_business) VALUES (?, ?, ?, ?, ?)", 
                       [models.Rilevazione.to_tuple(ed) for ed in energy_data])
    conn.commit()
    return cursor.rowcount

righe_inserite = inserisci_db(energy_data, conn)
print(f"Numero di record inseriti: {righe_inserite}" + (f" su {len(energy_data)} disponibili)"))
conn.close()