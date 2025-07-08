import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
import sys

# Configuración de conexión a la base de datos
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "carburantes")
DB_HOST = os.getenv("POSTGRES_HOST", "db")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

# URL de la API
url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"

# Cabeceras para evitar bloqueo por parte del servidor
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; carburantes-bot/1.0)"
}

try:
    print(f"[INFO] Solicitando datos desde la API...")
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()  # lanza error si el status no es 200

    data = response.json()
    df = pd.DataFrame(data['ListaEESSPrecio'])

    df.columns = df.columns.str.strip()
    for col in df.columns:
        df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]

    df['fecha_descarga'] = datetime.now().date()

    df.to_sql('precios_carburantes', con=engine, if_exists='append', index=False)
    print(f"[OK] Datos guardados correctamente. Registros: {len(df)}")

except requests.exceptions.RequestException as e:
    print(f"[ERROR] Fallo al obtener datos de la API: {e}", file=sys.stderr)

except Exception as e:
    print(f"[ERROR] Fallo inesperado: {e}", file=sys.stderr)

