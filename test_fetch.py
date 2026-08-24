import sys
sys.path.insert(0, "src")

from energy_dashboard.config import API_KEY
from energy_dashboard.fetch import fetch_generation_data
from energy_dashboard.storage_raw import save_raw

country_code = "10YIT-GRTN-----B"  # Italia
start = "202601010000" 
end = "202601020000"

if API_KEY is None:
     raise RuntimeError("ENTSOE_API_KEY non trovata: controlla il file .env")

xml_data = fetch_generation_data(country_code, start, end, API_KEY)
path = save_raw(xml_data, "IT")
print(f"Salvato in: {path}")