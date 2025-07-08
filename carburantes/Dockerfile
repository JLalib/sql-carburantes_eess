FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (incluye cron)
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean

# Instalar paquetes Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la app
COPY app /app

# Copiar y registrar la tarea cron
COPY crontab.txt /etc/cron.d/tarea-diaria
RUN chmod 0644 /etc/cron.d/tarea-diaria && crontab /etc/cron.d/tarea-diaria

# Iniciar cron en primer plano
CMD ["cron", "-f"]

