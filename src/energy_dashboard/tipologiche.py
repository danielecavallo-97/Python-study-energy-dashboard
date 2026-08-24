import sqlite3
from pathlib import Path
from dataclasses import dataclass
import datetime
import mapping

DB_PATH = Path("data/energy_data.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(Path("schema.sql").read_text())
    return conn

conn = get_connection()

#function tipologiche codice-descrizione
def inserisci_db(type_data: list, conn) -> int:
    cursor = conn.cursor()
    tabella = "FONTE"  # Sostituisci con il nome della tua tabella
    colonne = "(CODICE, DESCRIZIONE)"  # Sostituisci con i nomi delle colonne della tua tabella
    cursor.executemany("INSERT OR IGNORE INTO " + tabella + colonne + " VALUES (?, ?)", 
                       list(type_data))
    conn.commit()
    return cursor.rowcount

#function Area per classe
def inserisci_area_db(area_data: list, conn) -> int:
    cursor = conn.cursor()
    tabella = "AREA"
    colonne = "(AREA, CODICE, DESCRIZIONE, TIME_ZONE)"
    cursor.executemany("INSERT OR IGNORE INTO " + tabella + colonne + " VALUES (?, ?, ?, ?)", 
                       list(area_data))
    conn.commit()
    return cursor.rowcount


righe_area_inserite = inserisci_area_db([area.as_list() for area in mapping.Area], conn=conn)
righe_tipologiche_inserite = inserisci_db(list(mapping.PSRTYPE_MAPPINGS.items()), conn=conn)

print(f"Numero di record inseriti in AREA: {righe_area_inserite}")
print(f"Numero di record inseriti in TIPOLOGICHE: {righe_tipologiche_inserite}")
conn.close()