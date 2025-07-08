# ⛽ Proyecto: Importador Diario de Precios de Carburantes

Este proyecto descarga automáticamente, todos los días, los precios actualizados de las estaciones de servicio terrestres en España desde la API oficial del Ministerio para la Transición Ecológica. Los datos se almacenan en una base de datos PostgreSQL utilizando contenedores Docker y una tarea cron.

---

## 🧱 Estructura del proyecto

carburantes/
├── app/

│ ├── main.py # Script de descarga y guardado de datos

│ └── requirements.txt # Dependencias de Python
│
├── postgres/

│ ├── postgresql.conf # Configuración para exponer PostgreSQL a red

│ └── pg_hba.conf # Reglas de acceso externo
│
├── Dockerfile # Contenedor extractor (Python + cron)

├── crontab.txt # Tarea cron diaria

└── docker-compose.yml # Orquestación de servicios



---

## 🚀 Cómo ejecutar

### 1. Construir e iniciar los contenedores

docker-compose up -d --build
Esto iniciará:

carburantes_db: base de datos PostgreSQL expuesta en el puerto 5432

carburantes_extractor: contenedor con cron y main.py

### 2. Ejecutar una descarga manual (opcional)

docker exec -it carburantes_extractor python3 /app/main.py

### 3. Verificar datos insertados

docker exec -it carburantes_db psql -h 127.0.0.1 -U user -d carburantes

Dentro de psql:

SELECT COUNT(*) FROM precios_carburantes;

SELECT DISTINCT fecha_descarga FROM precios_carburantes ORDER BY fecha_descarga DESC;

🔌 Conexión desde herramientas BI

Desde otro equipo en la red (Power BI, Tableau, etc.), utiliza los siguientes parámetros:

Host	IP del servidor Docker (ej: 192.168.1.100)

Puerto	5432

Base de datos: carburantes

Usuario	user

Contraseña	password

🔧 Asegúrate de que:

docker-compose.yml expone el puerto 5432

postgresql.conf contiene: listen_addresses = '*'

pg_hba.conf permite conexiones externas: host all all 0.0.0.0/0 md5

🗓 Configuración de Cron

El archivo crontab.txt define la ejecución diaria del script a las 7:00 AM:

cron

0 7 * * * python3 /app/main.py >> /var/log/cron.log 2>&1
Puedes ajustar la hora si lo deseas. Después de cambiarlo, ejecuta:

docker-compose up -d --build

🛡 Recomendaciones

Cambia las credenciales predeterminadas de la base de datos antes de usarlo en producción.

Agrega lógica para evitar duplicados por fecha_descarga, si ejecutas múltiples veces al día.

Protege el acceso remoto con firewall o red VPN si estás fuera de una red local.

📊 Integraciones posibles

✅ Power BI

✅ Tableau

✅ Metabase (puedes agregarlo en Docker)

✅ pgAdmin

📄 Fuente de datos

Ministerio para la Transición Ecológica de España

API pública: https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/

🔧 Mantenimiento

Los datos se descargan automáticamente una vez al día.

Se acumulan en la tabla precios_carburantes con la fecha correspondiente.
