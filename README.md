# Energy Dashboard

Small study project: a pipeline that downloads electricity generation data from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/), stores it in SQLite, and produces a simple energy-mix report.

## Pipeline

```
ENTSO-E API ──► data/raw/*.xml ──► SQLite (data/energy_data.db) ──► pandas analysis ──► data/output/ (PNG + HTML)
   fetch.py       storage_raw.py      insert_db.py / tipologiche.py      analysis.py          report.py
```

| Module (`src/energy_dashboard/`) | Role |
|---|---|
| `config.py` | Loads `ENTSOE_API_KEY` from `.env`; raises if missing |
| `fetch.py` | Calls the ENTSO-E API (document type A75, process type A16: actual generation per type) |
| `storage_raw.py` | Saves the raw XML response as `data/raw/<COUNTRY>_<timestamp>.xml` |
| `mapping.py` | `Area` enum (EIC code, description, timezone) and PSR type (source) mappings |
| `models.py` | `Rilevazione` data model (one measurement) |
| `tipologiche.py` | Populates the lookup tables (`AREA`, `FONTE`, ...) |
| `insert_db.py` | Parses an XML file and inserts measurements into `rilevazioni` (`INSERT OR IGNORE`) |
| `analysis.py` | Loads data into pandas; computes energy mix (%) and daily trend per source |
| `report.py` | Generates a pie chart of the mix and an HTML report |

Database schema: see [schema.sql](schema.sql) (`DROP_schema.sql` drops it). The `rilevazioni` table has a `UNIQUE(PAESE, data, FONTE)` constraint, so re-importing the same file does not create duplicates.

## Requirements

- Python 3.14 (the committed bytecode targets 3.14)
- An ENTSO-E API key (request one via a Transparency Platform account)

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> `requirements.txt` is a UTF-16 `pip freeze` that includes an editable install of this project from GitHub. If pip fails on it, re-save it as UTF-8 or run `pip install -e .` plus the needed packages (`requests`, `python-dotenv`, `pandas`, `matplotlib`).

Create a `.env` file in the project root (it is git-ignored):

```
ENTSOE_API_KEY=your-api-key
```

## Usage

All commands must be run **from the project root**, because paths (`data/...`, `schema.sql`) are relative.

1. **Download raw data** (edit country code and dates in the script first):
   ```powershell
   python test_fetch.py
   ```
2. **Load lookup tables** (once):
   ```powershell
   python src/energy_dashboard/tipologiche.py
   ```
3. **Import XML into the DB** — the input file is currently hardcoded in `insert_db.py` (`data/raw/IT_20260828_113142.xml`):
   ```powershell
   python src/energy_dashboard/insert_db.py
   ```
4. **Analyse and report**:
   ```powershell
   python src/energy_dashboard/analysis.py   # prints mix and trend
   python src/energy_dashboard/report.py     # writes data/output/mix_IT.png and report_IT.html
   ```

## Known limitations

- Scripts execute on import (no `main()` / CLI); country, dates and input file are hardcoded.
- Modules use flat imports (`import models`), so they run as scripts from their folder context, not as an installed package.
- Analysis and report are only wired for Italy (`IT`).
- No automated tests (`test_fetch.py` is a manual download script).
- The database, raw XML and generated output are committed to the repository.

## Project structure

```
data/           raw XML, SQLite DB, generated output
src/energy_dashboard/   package source
schema.sql      DB schema
others/         exercises
```
