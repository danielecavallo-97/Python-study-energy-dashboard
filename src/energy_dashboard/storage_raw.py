from pathlib import Path
from datetime import datetime


def save_raw(content: str, country_code: str) -> Path:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"{country_code}_{timestamp}.xml"
    path.write_text(content, encoding="utf-8")
    return path