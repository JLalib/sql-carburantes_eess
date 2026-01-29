import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("/app/.env")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "db")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
headers = {"User-Agent": "Mozilla/5.0 (compatible; carburantes-bot/1.0)"}

try:
    print(f"[INFO] Solicitando datos desde la API...")
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["ListaEESSPrecio"])
    df.columns = df.columns.str.strip()
    for col in df.columns:
        df[col] = df[col].str.strip() if df[col].dtype == "object" else df[col]
    df["fecha_descarga"] = datetime.now().date()
    df.to_sql("precios_carburantes", engine, if_exists="append", index=False)
    print(f"[OK] Datos guardados: {len(df)}")

except Exception as e:
    print(f"[ERROR] {e}")
