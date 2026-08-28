import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("data/energy_data.db")

def load_db() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT R.PAESE, R.DATA, F.DESCRIZIONE FONTE, R.VALORE_MW, R.TIPO_BUSINESS " \
    "FROM rilevazioni as R, FONTE as F WHERE R.FONTE = F.CODICE"
    df = pd.read_sql_query(query, conn, parse_dates=["data"])
    conn.close()
    return df

def mix_energetico(df: pd.DataFrame, paese: str) -> pd.Series:
    """
    Calcola la percentuale di ciascuna fonte energetica per un determinato paese.
    
    Args:
        df (pd.DataFrame): DataFrame contenente i dati delle rilevazioni.
        paese (str): Il paese per cui calcolare il mix energetico.
        
    Returns:
        pd.Series: Serie con le fonti energetiche come indice e le percentuali come valori.
    """
    df_paese = df[df['PAESE'] == paese]
    totali = df_paese.groupby('FONTE')['VALORE_MW'].sum()
    percentuali = (totali / totali.sum() * 100).round(2)

    return percentuali.sort_values(ascending=False)

def trend_giornaliero(df: pd.DataFrame, paese: str, fonte: str) -> pd.DataFrame:
    """
    Calcola il trend giornaliero di una specifica fonte energetica per un determinato paese.
    
    Args:
        df (pd.DataFrame): DataFrame contenente i dati delle rilevazioni.
        paese (str): Il paese per cui calcolare il trend.
        fonte (str): La fonte energetica per cui calcolare il trend.
        
    Returns:
        pd.DataFrame: DataFrame con le date come indice e i valori giornalieri della fonte specificata.
    """
    subset = df[(df['PAESE'] == paese) & (df['FONTE'] == fonte)].copy()
    subset["giorno"] = subset["data"].dt.date
    trend = subset.groupby("giorno")['VALORE_MW'].mean().reset_index()
    
    return trend

rilevazioni = load_db()
mix_IT = mix_energetico(rilevazioni, "IT")
trend_IT = trend_giornaliero(rilevazioni, "IT", "Energy storage")
print(f"Mix energetico per l'Italia: {mix_IT}")
#print(rilevazioni)
print(f"trend giornaliero per l'Italia, storage: {trend_IT}")