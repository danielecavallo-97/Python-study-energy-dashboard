import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ENTSOE_API_KEY")

if not API_KEY:
    raise RuntimeError("ENTSOE_API_KEY non trovata: controlla il file .env")