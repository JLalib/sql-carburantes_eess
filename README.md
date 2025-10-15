# Proyecto: Carburantes - Descarga diaria desde API a PostgreSQL con Docker

Este proyecto descarga automáticamente cada día los datos de precios de carburantes en España desde la API oficial del Ministerio, y los guarda en una base de datos PostgreSQL dentro de Docker.

---

## 🚀 Tecnologías utilizadas

- Python 3.11
- Docker + Docker Compose
- PostgreSQL
- Cron (dentro de contenedor)
- SQLAlchemy + Pandas

---

## 📦 Estructura del proyecto

```
carburantes/
├── app/
│   ├── main.py              # Script principal de descarga
│   └── requirements.txt     # Dependencias Python
├── postgres/
│   ├── postgresql.conf      # Configuración opcional PostgreSQL
│   └── pg_hba.conf
├── crontab.txt              # Tarea programada diaria (cron)
├── Dockerfile               # Contenedor extractor
├── docker-compose.yml       # Orquesta servicios
├── .env                     # Variables de entorno
└── README.md
```

---

## ⚙️ Variables de entorno (.env)

```
POSTGRES_DB=carburantes
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
```

---

## 🛠 Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/JLalib/sql-carburantes_eess.git
cd carburantes
```

2. Ajusta `.env` si es necesario

3. Ejecuta todo con Docker Compose:

```bash
docker-compose up -d --build
```

Esto crea:
- PostgreSQL (`carburantes_db`) con persistencia
- Contenedor Python (`carburantes_extractor`) que ejecuta `main.py` diariamente (07:00 AM)

4. Ejecuta manualmente (opcional):

```bash
docker exec -it carburantes_extractor python3 /app/main.py
```

5. Verifica los datos:

```bash
docker exec -it carburantes_db psql -U user -d carburantes
```

```sql
SELECT COUNT(*) FROM precios_carburantes;
SELECT DISTINCT fecha_descarga FROM precios_carburantes ORDER BY fecha_descarga DESC;
```

---

## 🔁 Automatización diaria

La descarga diaria está programada por `cron` en el contenedor extractor. El resultado se guarda en `/var/log/cron.log` dentro del contenedor.

```bash
docker exec -it carburantes_extractor cat /var/log/cron.log
```

---

## 🛡 Protección contra duplicados

Antes de insertar, el script verifica si ya existen datos con la `fecha_descarga` actual.

---

## 📈 Ideas para expansión

- API de consulta (FastAPI)
- Dashboard visual (Streamlit, Dash)
- Exportación a CSV/Excel
- Conexión a Power BI / Grafana

---

## 🧑 Autor

Desarrollado por Genbyte · Octubre 2025
