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