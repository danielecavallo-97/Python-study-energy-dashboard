import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ENTSOE_API_KEY")

if not API_KEY:
    raise RuntimeError("ENTSOE_API_KEY non trovata: controlla il file .env")

import requests
import logging

logger = logging.getLogger(__name__)

def fetch_generation_data(country_code: str, start: str, end: str, api_key: str) -> str:
    """Scarica i dati di produzione elettrica per un paese in un intervallo di date.
    Ritorna il testo grezzo della risposta (XML)."""
    url = "https://web-api.tp.entsoe.eu/api"
    params = {
        "securityToken": api_key,
        "documentType": "A75",
        "processType": "A16",
        "in_Domain": country_code,
        "periodStart": start,
        "periodEnd": end,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        logger.error("Timeout durante la richiesta per %s", country_code)
        raise
    except requests.exceptions.HTTPError as e:
        logger.error("Errore HTTP %s per %s", e.response.status_code, country_code)
        raise

from pathlib import Path
from datetime import datetime


def save_raw(content: str, country_code: str) -> Path:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"{country_code}_{timestamp}.xml"
    path.write_text(content, encoding="utf-8")
    return path